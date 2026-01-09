# ML Claims Predictor - Frontend Integration Guide

This guide explains how to set up and run the ML Claims Predictor with the React frontend.

## 🎯 Overview

The ML integration allows users to:
1. Upload CSV files with claims data via a React frontend
2. Get ML predictions for pending claims (Paid/Denied probability)
3. View predictions in an interactive dashboard

## 📋 Prerequisites

- Python 3.11+ with virtual environment
- Node.js 16+ and npm
- Backend dependencies installed (see `requirements.txt`)
- Backend server running on port 8000

## 🚀 Quick Start

### Step 1: Backend Setup

1. **Ensure dependencies are installed:**
   ```bash
   # Activate virtual environment
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Linux/Mac

   # Install/update dependencies
   pip install -r requirements.txt
   ```

2. **Start the FastAPI server:**
   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at: `http://localhost:8000`
   - API Docs: `http://localhost:8000/docs`
   - Health Check: `http://localhost:8000/health`

### Step 2: Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure API URL (optional):**
   - Create `.env` file in `frontend/` directory
   - Add: `REACT_APP_API_URL=http://localhost:8000`
   - (Default is already set to `http://localhost:8000`)

4. **Start the React development server:**
   ```bash
   npm start
   ```

   The frontend will open at: `http://localhost:3000`

## 📡 API Endpoints

### POST `/reports/predict`

Upload a CSV file to get ML predictions for pending claims.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: `file` (CSV file)

**Response:**
```json
{
  "filename": "claims_export_2025.txt",
  "success": true,
  "total_claims": 15,
  "training_claims": 10,
  "pending_claims": 5,
  "predictions": [
    {
      "ClaimID": "C003",
      "Amount": 130.50,
      "Type": "Vision",
      "Date": "2025-01-17",
      "Predicted_Status": "Paid",
      "Denial_Probability": 0.15,
      "Confidence": 0.85
    }
  ],
  "summary": {
    "paid_count": 7,
    "denied_count": 3,
    "pending_count": 5
  }
}
```

## 🎨 Frontend Features

### Claims Predictor Component

The main component (`ClaimsPredictor.js`) provides:

1. **File Upload Interface**
   - Drag-and-drop or click to select CSV files
   - File validation (CSV/TXT only)
   - Loading states during processing

2. **Summary Dashboard**
   - Total claims count
   - Training vs pending claims
   - Paid/Denied/Pending breakdown

3. **Predictions Table**
   - Claim details (ID, Amount, Type, Date)
   - Predicted status (Paid/Denied)
   - Denial probability with visual progress bar
   - Confidence score

4. **Error Handling**
   - Clear error messages
   - Validation feedback
   - Network error handling

## 📁 File Structure

```
Claims-Reporting-Automation-System/
├── app/
│   ├── api/
│   │   └── reports.py          # API endpoints (includes /predict)
│   ├── ml/
│   │   └── claims_predictor.py # ML model logic
│   └── services/
│       └── ml_service.py       # ML service wrapper for API
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── ClaimsPredictor.js  # Main ML UI component
│   │   ├── api/
│   │   │   └── reports.js          # API client functions
│   │   ├── App.js                   # Main app component
│   │   └── index.js                 # React entry point
│   ├── package.json
│   └── tailwind.config.js
└── sample_data/
    └── claims_export_2025.txt   # Sample data for testing
```

## 🧪 Testing

### Test the ML Prediction

1. **Start both servers:**
   - Backend: `uvicorn app.main:app --reload`
   - Frontend: `npm start` (in frontend directory)

2. **Upload sample data:**
   - Go to `http://localhost:3000`
   - Click "Select CSV File"
   - Choose `sample_data/claims_export_2025.txt`
   - Click "Predict Claims"

3. **View results:**
   - See summary statistics
   - Review predictions table
   - Check denial probabilities

### Test via API Directly

```bash
# Using curl
curl -X POST "http://localhost:8000/reports/predict" \
  -F "file=@sample_data/claims_export_2025.txt"

# Or use the interactive docs
# Visit: http://localhost:8000/docs
# Try the POST /reports/predict endpoint
```

## 🔧 Troubleshooting

### Backend Issues

**Import Error: `app.ml.claims_predictor`**
- Ensure the directory is `app/ml/` (lowercase)
- Check that `__init__.py` exists in `app/ml/`

**ModuleNotFoundError: sklearn**
- Install: `pip install scikit-learn==1.3.2`
- Verify in `requirements.txt`

**File not found errors**
- Check file path resolution in `claims_predictor.py`
- Ensure sample data exists at `sample_data/claims_export_2025.txt`

### Frontend Issues

**CORS Errors**
- Add CORS middleware to FastAPI (see below)
- Check API URL in `.env` file

**API Connection Failed**
- Verify backend is running on port 8000
- Check `REACT_APP_API_URL` in `.env`
- Test backend health: `http://localhost:8000/health`

**Build Errors**
- Run `npm install` again
- Clear `node_modules` and reinstall
- Check Node.js version (16+)

## 🔒 CORS Configuration

If you encounter CORS errors, add this to `app/main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📊 Expected Data Format

The CSV file must contain these columns:
- `ClaimID`: Unique identifier
- `Status`: One of "Paid", "Denied", or "Pending"
- `Amount`: Numeric claim amount
- `Date`: Date in YYYY-MM-DD format
- `Type`: Claim type (e.g., "Medical", "Dental", "Vision")

Example:
```csv
ClaimID,Status,Amount,Date,Type
C001,Paid,550.25,2025-01-11,Medical
C002,Denied,200.00,2025-01-14,Dental
C003,Pending,130.50,2025-01-17,Vision
```

## 🚀 Production Deployment

### Backend
- Deploy FastAPI to Cloud Run, Heroku, or similar
- Set environment variables
- Ensure all dependencies are in `requirements.txt`

### Frontend
- Build: `npm run build`
- Deploy `build/` folder to Vercel, Netlify, or static hosting
- Update `REACT_APP_API_URL` to production API URL

## 📝 Next Steps

- [ ] Add model persistence (save/load trained models)
- [ ] Add prediction history to database
- [ ] Implement batch processing for large files
- [ ] Add export functionality (download predictions as CSV)
- [ ] Add authentication/authorization
- [ ] Improve error messages and validation

## 🆘 Support

For issues or questions:
1. Check the API docs: `http://localhost:8000/docs`
2. Review backend logs for errors
3. Check browser console for frontend errors
4. Verify all dependencies are installed
