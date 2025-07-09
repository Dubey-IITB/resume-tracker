# Resume Tracker Frontend

A modern React-based web application for tracking job applications and managing resumes with a beautiful, responsive UI.

## 🚀 Features

- **User Authentication**: Secure login and registration system
- **Dashboard**: Comprehensive overview of applications and candidates
- **Candidate Management**: Add, edit, and track candidate profiles
- **Job Posting Management**: Create and manage job listings
- **Resume Upload**: Drag-and-drop PDF resume upload functionality
- **AI-Powered Matching**: Intelligent candidate-job matching
- **Modern UI**: Material-UI components with responsive design
- **Real-time Updates**: Live data synchronization with backend

## 🛠️ Tech Stack

- **React 18** - Latest React with concurrent features
- **TypeScript** - Type-safe development
- **Vite** - Fast build tool and development server
- **Material-UI (MUI)** - Professional UI components
- **React Router** - Client-side routing
- **Axios** - HTTP client for API communication
- **Emotion** - CSS-in-JS styling solution

## 📋 Prerequisites

- Node.js (v16 or higher)
- npm (v7 or higher) or yarn
- Backend API running (see backend README)

## 🚀 Getting Started

### 1. Clone and Navigate

```bash
git clone <repository-url>
cd rt_frontend
```

### 2. Install Dependencies

```bash
npm install
# or
yarn install
```

### 3. Environment Configuration

Create a `.env` file in the root directory:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=Resume Tracker
```

### 4. Start Development Server

```bash
npm run dev
# or
yarn dev
```

The application will be available at [http://localhost:5173](http://localhost:5173)

## 📁 Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── common/         # Common components (Button, Input, etc.)
│   ├── forms/          # Form components
│   └── layout/         # Layout-specific components
├── contexts/           # React contexts for state management
│   ├── AuthContext.tsx # Authentication context
│   └── AppContext.tsx  # Global application context
├── hooks/              # Custom React hooks
│   ├── useAuth.ts      # Authentication hook
│   ├── useApi.ts       # API communication hook
│   └── useLocalStorage.ts # Local storage hook
├── layouts/            # Layout components
│   ├── MainLayout.tsx  # Main application layout
│   └── AuthLayout.tsx  # Authentication layout
├── pages/              # Page components
│   ├── Dashboard/      # Dashboard page
│   ├── Candidates/     # Candidate management pages
│   ├── Jobs/           # Job management pages
│   └── Auth/           # Authentication pages
├── services/           # API service functions
│   ├── api.ts          # Base API configuration
│   ├── auth.ts         # Authentication services
│   ├── candidates.ts   # Candidate services
│   └── jobs.ts         # Job services
├── types/              # TypeScript type definitions
│   ├── auth.ts         # Authentication types
│   ├── candidate.ts    # Candidate types
│   ├── job.ts          # Job types
│   └── api.ts          # API response types
├── utils/              # Utility functions
│   ├── constants.ts    # Application constants
│   ├── helpers.ts      # Helper functions
│   └── validation.ts   # Form validation
├── App.tsx             # Main App component
├── main.tsx            # Application entry point
└── vite-env.d.ts       # Vite type definitions
```

## 🧪 Available Scripts

- `npm run dev` - Start development server with hot reload
- `npm run build` - Build for production
- `npm run lint` - Run ESLint for code quality
- `npm run preview` - Preview production build locally
- `npm run type-check` - Run TypeScript type checking

## 🎨 UI Components

The application uses Material-UI components for a consistent and professional look:

- **Navigation**: AppBar with responsive drawer
- **Forms**: TextField, Select, Checkbox with validation
- **Data Display**: Tables, Cards, Lists for data presentation
- **Feedback**: Snackbars, Alerts, Progress indicators
- **Layout**: Grid system, Container, Box for responsive layouts

## 🔐 Authentication

The frontend implements JWT-based authentication:

- Login/Register forms with validation
- Protected routes with authentication guards
- Token storage in localStorage
- Automatic token refresh
- Logout functionality

## 📱 Responsive Design

The application is fully responsive and works on:

- Desktop computers (1200px+)
- Tablets (768px - 1199px)
- Mobile devices (320px - 767px)

## 🔄 State Management

State is managed using React Context API:

- **AuthContext**: Manages user authentication state
- **AppContext**: Manages global application state
- **Local State**: Component-specific state with useState/useReducer

## 🌐 API Integration

The frontend communicates with the backend API using:

- **Axios**: HTTP client with interceptors
- **Type-safe API calls**: TypeScript interfaces for all API responses
- **Error handling**: Centralized error handling and user feedback
- **Loading states**: Loading indicators for better UX

## 🧪 Testing

### Running Tests

```bash
npm run test
```

### Test Structure

- Unit tests for components
- Integration tests for API calls
- E2E tests for critical user flows

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

### Deployment Options

1. **Static Hosting** (Netlify, Vercel, GitHub Pages)
2. **Docker Container**
3. **Traditional Web Server** (Nginx, Apache)

### Environment Variables for Production

```env
VITE_API_BASE_URL=https://your-api-domain.com
VITE_APP_NAME=Resume Tracker
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow TypeScript best practices
- Use functional components with hooks
- Implement proper error handling
- Write meaningful commit messages
- Add tests for new features

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## 🆘 Support

For support and questions:
- Check the [main README](../README.md) for overall project information
- Review the [backend README](../rt_backend/README.md) for API documentation
- Open an issue on the repository

## 🔗 Related Links

- [Backend API Documentation](../rt_backend/README.md)
- [Main Project README](../README.md)
- [Material-UI Documentation](https://mui.com/)
- [React Documentation](https://react.dev/)
