# Resume Tracker

A comprehensive full-stack application for tracking job applications, managing resumes, and matching candidates with job descriptions using AI-powered analysis.

## 🚀 Overview

Resume Tracker is a modern web application that helps recruiters and HR professionals efficiently manage the hiring process. The system combines a React-based frontend with a FastAPI backend to provide:

- **Resume Management**: Upload, store, and organize candidate resumes
- **Job Posting Management**: Create and manage job listings
- **AI-Powered Matching**: Intelligent candidate-job matching using local LLM
- **Candidate Tracking**: Comprehensive candidate profiles and application status
- **Modern UI**: Responsive, user-friendly interface built with Material-UI

## 🏗️ Architecture

The project follows a microservices architecture with clear separation of concerns:

```
resume-tracker/
├── rt_frontend/          # React TypeScript frontend
│   ├── src/
│   ├── package.json
│   └── README.md
├── rt_backend/           # FastAPI Python backend
│   ├── app/
│   ├── requirements.txt
│   └── README.md
└── README.md            # This file
```

### Frontend (rt_frontend)
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **UI Library**: Material-UI (MUI)
- **State Management**: React Context API
- **Routing**: React Router DOM
- **HTTP Client**: Axios

### Backend (rt_backend)
- **Framework**: FastAPI
- **Database**: SQLite (configurable)
- **ORM**: SQLAlchemy
- **AI Integration**: Ollama (local LLM)
- **Authentication**: JWT-based
- **File Processing**: PDF extraction and analysis

## 🛠️ Tech Stack

### Frontend
- React 18
- TypeScript
- Vite
- Material-UI
- React Router
- Axios

### Backend
- FastAPI
- SQLAlchemy
- PyPDF2
- Ollama (Local LLM)
- Pydantic
- Uvicorn

## 📋 Prerequisites

Before running this application, ensure you have:

- **Node.js** (v16 or higher)
- **Python** (3.8 or higher)
- **Ollama** (for local LLM functionality)
- **Git**

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd resume-tracker
```

### 2. Backend Setup

```bash
cd rt_backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (if needed)
cp .env.example .env  # Create if not exists

# Run the backend
python main.py
# Or with uvicorn
uvicorn main:app --reload
```

The backend will be available at `http://localhost:8000`

### 3. Frontend Setup

```bash
cd rt_frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

### 4. Ollama Setup (Required for AI Features)

1. Install Ollama from [ollama.ai](https://ollama.ai)
2. Pull a model (e.g., llama2):
   ```bash
   ollama pull llama2
   ```
3. Start Ollama service:
   ```bash
   ollama serve
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `rt_backend` directory:

```env
# Database
DATABASE_URL=sqlite:///./app.db

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# JWT Settings
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Settings
ALLOWED_ORIGINS=http://localhost:5173
```

## 📁 Project Structure

### Frontend Structure
```
rt_frontend/
├── src/
│   ├── components/     # Reusable UI components
│   ├── contexts/       # React contexts for state management
│   ├── hooks/          # Custom React hooks
│   ├── layouts/        # Layout components
│   ├── pages/          # Page components
│   ├── services/       # API service functions
│   ├── types/          # TypeScript type definitions
│   ├── App.tsx         # Main application component
│   └── main.tsx        # Application entry point
├── package.json
└── vite.config.ts
```

### Backend Structure
```
rt_backend/
├── app/
│   ├── api/            # API route handlers
│   ├── core/           # Core configuration
│   ├── db/             # Database models and session
│   ├── services/       # Business logic services
│   └── utils/          # Utility functions
├── tests/              # Test files
├── main.py             # Application entry point
└── requirements.txt
```

## 🧪 Testing

### Backend Tests
```bash
cd rt_backend
python -m pytest
```

### Frontend Tests
```bash
cd rt_frontend
npm run test
```

## 🚀 Deployment

### Backend Deployment
1. Build the application:
   ```bash
   pip install -r requirements.txt
   ```
2. Set production environment variables
3. Use a production ASGI server like Gunicorn:
   ```bash
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

### Frontend Deployment
1. Build the application:
   ```bash
   npm run build
   ```
2. Serve the `dist` folder with a web server like Nginx

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Check the individual README files in `rt_frontend/` and `rt_backend/`
- Review the API documentation at `http://localhost:8000/docs` when the backend is running
- Open an issue on the repository

## 🔄 Development Workflow

1. **Backend Development**: Work in the `rt_backend/` directory
2. **Frontend Development**: Work in the `rt_frontend/` directory
3. **API Testing**: Use the interactive docs at `http://localhost:8000/docs`
4. **Database Changes**: Update models in `rt_backend/app/db/models.py`

## 🎯 Key Features

- **Resume Processing**: Upload and extract information from PDF resumes
- **AI Matching**: Intelligent candidate-job matching using local LLM
- **Candidate Management**: Comprehensive candidate profiles and tracking
- **Job Management**: Create and manage job postings
- **Modern UI**: Responsive design with Material-UI components
- **Scalable Architecture**: Microservices-based design for easy scaling 