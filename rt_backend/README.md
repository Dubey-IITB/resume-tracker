# Resume Tracker Backend API

A robust FastAPI-based backend service for processing resumes, matching candidates with job descriptions, and providing detailed analysis using local LLM capabilities.

## 🚀 Features

### Resume Processing
- **PDF Text Extraction**: Extract and clean text from PDF resumes
- **Email Extraction**: Intelligent email extraction using regex patterns and LLM
- **Fallback Mechanisms**: Synthetic email generation when extraction fails
- **Text Cleaning**: Robust text formatting and cleaning

### Candidate Management
- **Profile Storage**: Comprehensive candidate profile management
- **CTC Tracking**: Current and expected CTC management
- **Resume Storage**: Secure resume text storage and retrieval
- **Bulk Operations**: Process multiple resumes simultaneously

### AI-Powered Job Matching
- **Intelligent Matching**: Match candidates against job descriptions
- **Budget Analysis**: Budget-based candidate ranking
- **Technical Assessment**: Skills and experience evaluation
- **Salary Compatibility**: Comprehensive salary analysis
- **Detailed Reports**: In-depth candidate fit analysis

### Local LLM Integration (Ollama)
- **Resume Ranking**: AI-powered candidate ranking
- **Email Extraction**: LLM-assisted email identification
- **Candidate Comparison**: Detailed candidate comparison
- **Job Description Analysis**: Intelligent job-candidate matching
- **No External Dependencies**: Complete local AI processing

## 🛠️ Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: Powerful ORM for database operations
- **PyPDF2**: Robust PDF processing and text extraction
- **Ollama**: Local LLM serving for AI operations
- **Pydantic**: Data validation and serialization
- **Uvicorn**: Lightning-fast ASGI server
- **Python-multipart**: File upload handling
- **Alembic**: Database migration management

## 📋 Prerequisites

- Python 3.8 or higher
- Ollama (for local LLM functionality)
- Virtual environment tool (venv, conda, etc.)

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Ollama Setup

```bash
# Install Ollama (if not already installed)
# Visit https://ollama.ai for installation instructions

# Pull a model (e.g., llama2)
ollama pull llama2

# Start Ollama service
ollama serve
```

### 3. Configuration

Create a `.env` file in the backend directory:

```env
# Database Configuration
DATABASE_URL=sqlite:///./app.db

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# JWT Settings
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Settings
ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# File Upload Settings
MAX_FILE_SIZE=10485760  # 10MB
UPLOAD_DIR=./uploads
```

### 4. Run the Application

```bash
# Option 1: Direct Python execution
python main.py

# Option 2: Using uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Option 3: Production with gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, you can access:

- **Interactive API Docs**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh access token

### Resume Processing
- `POST /api/process-and-match` - Process resumes and match against job description
- `POST /api/extract-email` - Extract email from resume text using LLM
- `POST /api/rank` - Compare multiple resumes for a specific job

### Candidate Management
- `GET /api/candidates` - List all candidates
- `POST /api/candidates` - Create a new candidate
- `GET /api/candidates/{id}` - Get candidate details
- `PUT /api/candidates/{id}` - Update candidate
- `DELETE /api/candidates/{id}` - Delete candidate
- `POST /api/create-candidates-from-pdfs` - Bulk create candidates from PDF resumes

### Job Management
- `GET /api/jobs` - List all jobs
- `POST /api/jobs` - Create a new job
- `GET /api/jobs/{id}` - Get job details
- `PUT /api/jobs/{id}` - Update job
- `DELETE /api/jobs/{id}` - Delete job

## 📁 Project Structure

```
rt_backend/
├── app/
│   ├── api/                    # API route handlers
│   │   ├── routes/            # Route modules
│   │   │   ├── auth.py        # Authentication routes
│   │   │   ├── candidates.py  # Candidate routes
│   │   │   └── jobs.py        # Job routes
│   │   └── dependencies.py    # API dependencies
│   ├── core/                  # Core configuration
│   │   ├── config.py          # Application settings
│   │   ├── security.py        # Security utilities
│   │   └── exceptions.py      # Custom exceptions
│   ├── db/                    # Database layer
│   │   ├── models.py          # SQLAlchemy models
│   │   ├── session.py         # Database session
│   │   └── base.py            # Base model class
│   ├── services/              # Business logic
│   │   ├── auth_service.py    # Authentication logic
│   │   ├── candidate_service.py # Candidate operations
│   │   ├── job_service.py     # Job operations
│   │   ├── pdf_service.py     # PDF processing
│   │   └── ollama_service.py  # LLM integration
│   ├── schemas/               # Pydantic schemas
│   │   ├── auth.py            # Authentication schemas
│   │   ├── candidate.py       # Candidate schemas
│   │   ├── job.py             # Job schemas
│   │   └── common.py          # Common schemas
│   └── utils/                 # Utility functions
│       ├── pdf_utils.py       # PDF processing utilities
│       ├── text_utils.py      # Text processing utilities
│       └── validation.py      # Validation helpers
├── tests/                     # Test files
├── uploads/                   # File upload directory
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── schema.sql                # Database schema
└── README.md                 # This file
```

## 🗄️ Database

### Models

- **Candidates**: Store candidate information and resume data
- **Jobs**: Job postings and requirements
- **CandidateJobMatches**: Matching results and analysis
- **Users**: User authentication and profiles

### Database Setup

```bash
# The database will be created automatically on first run
# For manual setup:
python -c "from app.db.session import engine; from app.db import models; models.Base.metadata.create_all(bind=engine)"
```

### Migrations

```bash
# Initialize Alembic (if not already done)
alembic init alembic

# Create a migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head
```

## 🤖 Ollama Integration

### Configuration

The system uses Ollama for local LLM operations:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
```

### Supported Operations

- **Email Extraction**: Extract emails from resume text
- **Candidate Analysis**: Analyze candidate skills and experience
- **Job Matching**: Match candidates with job descriptions
- **Resume Ranking**: Rank multiple candidates for a position

### Model Recommendations

- **llama2**: Good balance of performance and resource usage
- **llama2:7b**: Faster inference, lower resource usage
- **llama2:13b**: Better quality, higher resource usage

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=app

# Run specific test file
python -m pytest tests/test_api.py

# Run with verbose output
python -m pytest -v
```

### Test Files

- `test_api.py` - API endpoint testing
- `test_ollama.py` - Ollama integration testing
- `test_extract_email_api.py` - Email extraction testing
- `test_candidate_creation.py` - Candidate creation testing
- `test_end_to_end.py` - End-to-end workflow testing
- `test_live_endpoints.py` - Live API testing

### Test Data

```bash
# Populate database with test data
python populate_db.py

# Create test PDFs
python create_test_pdfs.py
```

## 🔒 Security

### Authentication

- JWT-based authentication
- Password hashing with bcrypt
- Token refresh mechanism
- Secure session management

### File Upload Security

- File type validation
- File size limits
- Secure file storage
- Virus scanning (recommended for production)

### API Security

- CORS configuration
- Rate limiting (recommended for production)
- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy

## 🚀 Deployment

### Production Setup

1. **Environment Variables**:
   ```env
   DATABASE_URL=postgresql://user:password@localhost/dbname
   SECRET_KEY=your-production-secret-key
   ALLOWED_ORIGINS=https://yourdomain.com
   ```

2. **Database**: Use PostgreSQL for production
3. **File Storage**: Use cloud storage (AWS S3, Google Cloud Storage)
4. **Process Manager**: Use systemd or supervisor
5. **Reverse Proxy**: Use Nginx or Apache

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Performance Optimization

- Database connection pooling
- Caching with Redis (recommended)
- Async file processing
- Load balancing for high traffic

## 🔧 Error Handling

The API implements comprehensive error handling:

- **HTTP Status Codes**: Proper status code responses
- **Error Messages**: Clear, actionable error messages
- **Logging**: Structured logging for debugging
- **Graceful Degradation**: Fallback mechanisms for LLM failures

## 📊 Monitoring

### Health Checks

- `GET /health` - Basic health check
- `GET /health/detailed` - Detailed system status

### Logging

- Structured logging with JSON format
- Log levels: DEBUG, INFO, WARNING, ERROR
- Request/response logging
- Performance metrics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write comprehensive tests
- Update documentation
- Use type hints
- Handle errors gracefully

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Check the [main README](../README.md) for overall project information
- Review the [frontend README](../rt_frontend/README.md) for frontend details
- Open an issue on the repository

## 🔗 Related Links

- [Frontend Documentation](../rt_frontend/README.md)
- [Main Project README](../README.md)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Ollama Documentation](https://ollama.ai/docs)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)