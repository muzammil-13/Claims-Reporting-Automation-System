# Claims Reporting Frontend

React frontend for the Claims Reporting Automation System with ML prediction capabilities.

## Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Configure API URL:**
   - Copy `.env.example` to `.env`
   - Update `REACT_APP_API_URL` if your backend is running on a different port

3. **Start development server:**
   ```bash
   npm start
   ```

The app will open at http://localhost:3000

## Features

- **Claims Prediction**: Upload CSV files to predict outcomes for pending claims
- **Interactive Dashboard**: View predictions with probability scores and confidence levels
- **Real-time Processing**: Get instant ML predictions for your claims data

## API Integration

The frontend communicates with the FastAPI backend at:
- Default: `http://localhost:8000`
- Configure via `REACT_APP_API_URL` environment variable

## Build for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` folder.
