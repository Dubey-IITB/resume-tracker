-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE
);

-- Create jobs table
CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    jd_text TEXT,
    min_budget DECIMAL(10,2),
    max_budget DECIMAL(10,2),
    status VARCHAR(50) DEFAULT 'active',
    recruiter_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Create candidates table
CREATE TABLE candidates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    resume_path VARCHAR(255),
    resume_text TEXT,
    current_ctc DECIMAL(10,2),
    expected_ctc DECIMAL(10,2),
    additional_info TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Create candidate_job_match table (junction table)
CREATE TABLE candidate_job_match (
    candidate_id INTEGER REFERENCES candidates(id),
    job_id INTEGER REFERENCES jobs(id),
    jd_match_score DECIMAL(5,2),
    comparative_score DECIMAL(5,2),
    overall_score DECIMAL(5,2),
    salary_match_score DECIMAL(5,2),
    technical_match_score DECIMAL(5,2),
    experience_match_score DECIMAL(5,2),
    strengths TEXT,
    weaknesses TEXT,
    salary_analysis TEXT,
    recommendation TEXT,
    comparative_analysis TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (candidate_id, job_id)
);

-- Create indexes for better query performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_jobs_title ON jobs(title);
CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_candidates_name ON candidates(name);
CREATE INDEX idx_candidates_email ON candidates(email);
CREATE INDEX idx_candidate_job_match_scores ON candidate_job_match(overall_score, technical_match_score, experience_match_score);

-- Create trigger for updating updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for all tables with updated_at
CREATE TRIGGER update_jobs_updated_at
    BEFORE UPDATE ON jobs
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_candidates_updated_at
    BEFORE UPDATE ON candidates
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column(); 