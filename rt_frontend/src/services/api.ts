import axios, { AxiosInstance, AxiosError } from 'axios';
import {
    User,
    LoginRequest,
    LoginResponse,
    Candidate,
    Job,
    JobCreate,
    ProcessAndMatchResponse,
    RankingResponse,
} from '../types';

// API base URL - defaults to local development
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Create axios instance
const api: AxiosInstance = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add auth token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor for error handling
api.interceptors.response.use(
    (response) => response,
    (error: AxiosError) => {
        if (error.response?.status === 401) {
            // Clear token and redirect to login
            localStorage.removeItem('access_token');
            localStorage.removeItem('user');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

// ============= Auth API =============

export const authApi = {
    login: async (credentials: LoginRequest): Promise<LoginResponse> => {
        const response = await api.post('/login', credentials);
        const data: LoginResponse = response.data;

        // Store token and user
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('user', JSON.stringify(data.user));

        return data;
    },

    logout: () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
    },

    getCurrentUser: (): User | null => {
        const userStr = localStorage.getItem('user');
        return userStr ? JSON.parse(userStr) : null;
    },

    isAuthenticated: (): boolean => {
        return !!localStorage.getItem('access_token');
    },
};

// ============= Candidates API =============

export const candidatesApi = {
    getAll: async (): Promise<Candidate[]> => {
        const response = await api.get('/candidates');
        return response.data;
    },

    getByEmail: async (email: string): Promise<Candidate> => {
        const response = await api.get(`/candidates/${email}`);
        return response.data;
    },

    uploadResumes: async (
        files: File[],
        currentCtcs: number[],
        expectedCtcs: number[]
    ): Promise<Candidate[]> => {
        const formData = new FormData();
        files.forEach((file) => {
            formData.append('files', file);
        });
        currentCtcs.forEach((ctc) => {
            formData.append('current_ctcs', ctc.toString());
        });
        expectedCtcs.forEach((ctc) => {
            formData.append('expected_ctcs', ctc.toString());
        });

        const response = await api.post('/create-candidates-from-pdfs', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    },

    processAndMatch: async (
        jobDescription: string,
        budget: number,
        files: File[],
        currentCtcs: string[],
        expectedCtcs: string[]
    ): Promise<ProcessAndMatchResponse> => {
        const formData = new FormData();
        formData.append('job_description', jobDescription);
        formData.append('budget', budget.toString());
        files.forEach((file) => {
            formData.append('files', file);
        });
        currentCtcs.forEach((ctc) => {
            formData.append('current_ctcs', ctc);
        });
        expectedCtcs.forEach((ctc) => {
            formData.append('expected_ctcs', ctc);
        });

        const response = await api.post('/candidates/process-and-match', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    },
};

// ============= Jobs API =============

export const jobsApi = {
    getAll: async (): Promise<Job[]> => {
        const response = await api.get('/jobs');
        return response.data;
    },

    getById: async (id: number): Promise<Job> => {
        const response = await api.get(`/jobs/${id}`);
        return response.data;
    },

    create: async (job: JobCreate): Promise<Job> => {
        const response = await api.post('/jobs', job);
        return response.data;
    },

    update: async (id: number, job: Partial<JobCreate>): Promise<Job> => {
        const response = await api.put(`/jobs/${id}`, job);
        return response.data;
    },

    delete: async (id: number): Promise<void> => {
        await api.delete(`/jobs/${id}`);
    },
};

// ============= Rankings API =============

export const rankingsApi = {
    rankByJob: async (jobId: number): Promise<RankingResponse> => {
        const response = await api.post(`/rank-by-job/${jobId}`);
        return response.data;
    },

    getRankings: async (jobId: number): Promise<RankingResponse> => {
        const response = await api.get(`/rankings/${jobId}`);
        return response.data;
    },

    updateStatus: async (
        candidateEmail: string,
        jobId: number,
        status: 'active' | 'saved' | 'rejected'
    ): Promise<void> => {
        await api.patch(
            `/candidate-match/${encodeURIComponent(candidateEmail)}/${jobId}/status`,
            { status }
        );
    },
};

// Export the axios instance for custom requests
export default api;
