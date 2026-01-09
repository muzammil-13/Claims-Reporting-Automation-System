# Claims Reporting Automation System  
A cloud‑native simulation of a real enterprise workflow: **mainframe output → report generation (Excel/PDF) → cloud upload → ML-powered predictions → dashboard for download**.

This project modernizes a legacy reporting pipeline using **FastAPI, React, GCP Cloud Run, Cloud Storage, PostgreSQL, and Python automation** — all built using **mock data** (fully safe and compliant).

---

## 🚀 Features

### 🔹 End‑to‑End Automated Reporting  
- Upload mock claim files (CSV/TXT)  
- Parse, clean, and validate data  
- Generate **Excel + PDF** reports  
- Upload reports to **Google Cloud Storage**  
- View and download reports from a modern UI  

### 🤖 ML-Powered Claims Prediction
- **Predict claim outcomes** (Paid/Denied) for pending claims
- **Random Forest** classification model
- **Probability scores** and confidence levels
- **Interactive dashboard** with visual predictions
- Real-time processing via React frontend

### 🔹 Cloud‑Native Architecture  
- Backend: **FastAPI** on Cloud Run  
- Frontend: **React** dashboard with Tailwind CSS
- Storage: Cloud Storage buckets  
- Database: Cloud SQL (PostgreSQL) or SQLite (default)
- Scheduled jobs via Cloud Scheduler  

### 🔹 Enterprise‑Grade Modules  
- Clean folder architecture  
- ML model integration
- RESTful API design
- Error handling and validation
- CORS-enabled for frontend integration  

---

## 📸 Screenshots

### ML Claims Prediction Dashboard

![Claims Prediction UI](screenshots/Claims-Reporting-Automation-System.png)

*Interactive dashboard showing ML predictions for pending claims with probability scores and confidence levels.*

### API Docs
![FastAPI interactive documentation](screenshots/Claims-Reporting-Automation-System-Swagger-UI.png)
   *- Shows the `/docs` endpoint*

---

## 🧱 Architecture Overview  

Client (React)  
→ Backend API (FastAPI)  
→ Data Processing (pandas)  
→ Report Generators (Excel/PDF)  
→ Cloud Storage (GCP)  
→ Database (PostgreSQL)

### High-Level Workflow  
```
Upload File → Parse & Clean → Aggregate Data 
→ Excel/PDF Generation → Upload to GCP → Metadata Saved 
→ Dashboard Download

ML Prediction Flow:
Upload CSV → Feature Engineering → Train Model 
→ Predict Pending Claims → Display Results in Dashboard
```

---

## 🛠️ Tech Stack

### Frontend  
- React  
- Tailwind CSS  
- Axios  
- Vercel / Cloud Run deployment

### Backend  
- FastAPI  
- Python (pandas, numpy, scikit-learn, openpyxl, reportlab)  
- SQLAlchemy  
- Pydantic  
- Google Cloud Storage SDK
- Machine Learning (Random Forest Classifier)

### Cloud  
- Cloud Run  
- Cloud Storage  
- Cloud SQL  
- Cloud Scheduler  

---

## 📁 Folder Structure  

```
Claims-Reporting-Automation-System/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── api/
│   │   └── reports.py         # API endpoints (upload, predict, list)
│   ├── ml/
│   │   └── claims_predictor.py # ML model for predictions
│   ├── models/
│   │   └── report.py          # SQLAlchemy Report model
│   ├── db/
│   │   ├── base.py            # Database base
│   │   └── session.py        # Database session
│   └── services/
│       ├── excel_generator.py # Excel/PDF report generation
│       ├── ml_service.py      # ML service wrapper
│       └── storage.py        # Google Cloud Storage
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── ClaimsPredictor.js  # ML prediction UI
│   │   ├── api/
│   │   │   └── reports.js         # API client
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── tailwind.config.js
├── sample_data/
│   └── claims_export_2025.txt # Sample claims data
├── requirements.txt            # Python dependencies
└── README.md
```

---

## 🧪 Sample Mock Data

Sample data is located in `sample_data/claims_export_2025.txt`:

```csv
ClaimID,Status,Amount,Date,Type
C001,Paid,550.25,2025-01-11,Medical
C002,Denied,200.00,2025-01-14,Dental
C003,Pending,130.50,2025-01-17,Vision
C004,Paid,1250.75,2025-01-18,Medical
...
```

**Required Columns:**
- `ClaimID`: Unique identifier
- `Status`: One of "Paid", "Denied", or "Pending"
- `Amount`: Numeric claim amount
- `Date`: Date in YYYY-MM-DD format
- `Type`: Claim type (e.g., "Medical", "Dental", "Vision")

---

## 🔌 API Endpoints  

### Reports  
- `POST /reports/upload` - Upload CSV file, generate Excel/PDF reports, upload to GCS
- `POST /reports/predict` - Upload CSV file, get ML predictions for pending claims
- `GET /reports` - List all processed reports

### System  
- `GET /health` - Health check endpoint

### Interactive API Documentation
- `GET /docs` - Swagger UI (FastAPI auto-generated docs)
- `GET /redoc` - ReDoc documentation  

---

## 📜 Environment Variables  

Create `.env` file in project root:

```env
# Database (optional - defaults to SQLite)
DATABASE_URL=postgresql://user:pass@host:port/db

# Google Cloud Storage (required for file uploads)
GCP_BUCKET_NAME=your-bucket-name

# Frontend API URL (optional)
REACT_APP_API_URL=http://localhost:8000
```

**Note:** See `SETUP_ENV.md` for detailed setup instructions.

---

## ▶️ How to Run Locally  

### Prerequisites
- Python 3.11+ with virtual environment
- Node.js 16+ and npm
- (Optional) PostgreSQL for production-like setup

### Backend Setup

1. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Linux/Mac
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   - Copy `.env.example` to `.env` (if exists)
   - Set `DATABASE_URL` (optional - defaults to SQLite)
   - Set `GCP_BUCKET_NAME` (required for file uploads)

4. **Start the server:**
   ```bash
   uvicorn app.main:app --reload
   ```
   
   Server runs at: `http://localhost:8000`
   - API Docs: `http://localhost:8000/docs`
   - Health Check: `http://localhost:8000/health`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm start
   ```
   
   Frontend runs at: `http://localhost:3000`

### Quick Test

1. Start backend: `uvicorn app.main:app --reload`
2. Start frontend: `cd frontend && npm start`
3. Open `http://localhost:3000`
4. Upload `sample_data/claims_export_2025.txt` for ML predictions

---

## ☁️ Deployment

### Backend on Cloud Run  
- Build Docker image  
- Push to Container Registry  
- Deploy with Cloud SQL + Cloud Storage permissions  

### Frontend  
- Deploy to Vercel or Cloud Run  

### Scheduler  
- Cloud Scheduler → calls `/reports/generate` on cron  

---

## 📚 Documentation

- **[ML Integration Guide](ML_INTEGRATION_GUIDE.md)** - Complete guide for ML prediction feature
- **[Environment Setup](SETUP_ENV.md)** - Detailed environment variable configuration
- **[Virtual Environment Guide](VENV_GUIDE.md)** - Python virtual environment setup

## 📌 Features & Capabilities

### Current Features
✅ CSV/TXT file upload and validation  
✅ Excel and PDF report generation  
✅ Google Cloud Storage integration  
✅ ML-powered claims prediction  
✅ Interactive React dashboard  
✅ RESTful API with auto-generated docs  
✅ SQLite (default) or PostgreSQL support  

### Future Enhancements  
- [ ] Model persistence (save/load trained models)
- [ ] Prediction history in database
- [ ] Batch processing for large files
- [ ] Export predictions as CSV
- [ ] Role-based access control  
- [ ] Email notifications  
- [ ] Additional file formats  
- [ ] Multi-file parallel processing  

---

## 📄 License  
MIT License

---

## 🤝 Contributions  
PRs and improvements are welcome!

---

## 🧪 Testing the ML Prediction

1. **Start both servers** (backend and frontend)
2. **Upload sample data:**
   - Go to `http://localhost:3000`
   - Click "Select CSV/TXT File"
   - Choose `sample_data/claims_export_2025.txt`
   - Click "Predict Claims"
3. **View results:**
   - See summary statistics
   - Review predictions table with probabilities
   - Check denial risk scores

## 🔧 Troubleshooting

### Common Issues

**Import errors (sklearn, numpy):**
```bash
pip install scikit-learn==1.3.2 numpy==1.26.4
```

**CORS errors:**
- Backend includes CORS middleware for `localhost:3000`
- Check `app/main.py` for CORS configuration

**File not found:**
- Ensure `sample_data/claims_export_2025.txt` exists
- Check file path in ML predictor script

**Frontend connection errors:**
- Verify backend is running on port 8000
- Check `REACT_APP_API_URL` in frontend `.env`

See [ML_INTEGRATION_GUIDE.md](ML_INTEGRATION_GUIDE.md) for detailed troubleshooting.

## ⭐ Acknowledgment  
This project is a modern cloud implementation inspired by the typical **mainframe → reporting → SharePoint** workflow used in enterprise environments, redesigned using modern engineering practices for learning and demonstration.

---

**Built with:** FastAPI • React • Tailwind CSS • scikit-learn • pandas • PostgreSQL/SQLite • Google Cloud Storage
