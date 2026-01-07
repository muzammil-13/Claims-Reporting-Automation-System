# Claims Reporting Automation System  
A cloud‑native simulation of a real enterprise workflow: **mainframe output → report generation (Excel/PDF) → cloud upload → dashboard for download**.

This project modernizes a legacy reporting pipeline using **FastAPI, React, GCP Cloud Run, Cloud Storage, PostgreSQL, and Python automation** — all built using **mock data** (fully safe and compliant).

---

## 🚀 Features

### 🔹 End‑to‑End Automated Reporting  
- Upload mock claim files (CSV/TXT)  
- Parse, clean, and validate data  
- Generate **Excel + PDF** reports  
- Upload reports to **Google Cloud Storage**  
- View and download reports from a modern UI  

### 🔹 Cloud‑Native Architecture  
- Backend: **FastAPI** on Cloud Run  
- Frontend: **React** dashboard  
- Storage: Cloud Storage buckets  
- Database: Cloud SQL (PostgreSQL)  
- Scheduled jobs via Cloud Scheduler  

### 🔹 Enterprise‑Grade Modules  
- JWT Authentication  
- Background processing  
- Structured logging  
- Clean folder architecture  
- Realistic reporting pipeline  

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
- Python (pandas, openpyxl, reportlab/fpdf)  
- SQLAlchemy  
- Pydantic  
- Google Cloud Storage SDK

### Cloud  
- Cloud Run  
- Cloud Storage  
- Cloud SQL  
- Cloud Scheduler  

---

## 📁 Folder Structure  

```
backend/
  app/
    main.py
    api/
      auth.py
      reports.py
    core/
      config.py
      security.py
    models/
      user.py
      report.py
    db/
      base.py
      session.py
    services/
      parser.py
      excel_generator.py
      pdf_generator.py
      storage.py
      scheduler.py
    utils/
      logger.py
      helpers.py
  requirements.txt
  Dockerfile

frontend/
  src/
    components/
      Upload.js
      ReportList.js
      ReportCard.js
    pages/
      Login.js
      Dashboard.js
    api/
      auth.js
      reports.js
  package.json
  tailwind.config.js
  Dockerfile
```

---

## 🧪 Sample Mock Data (Example)

Store inside `/backend/sample_data/`:

```
ClaimID,Status,Amount,Date,Type
C001,Paid,550.25,2025-01-11,Medical
C002,Denied,200.00,2025-01-14,Dental
C003,Pending,130.50,2025-01-17,Vision
```

---

## 🔌 API Endpoints  

### Auth
POST /auth/signup  
POST /auth/login  

### Reports  
POST /reports/upload  
GET /reports  
GET /reports/{id}  
POST /reports/generate  

### System  
GET /health  

---

## 📜 Environment Variables  

Create `.env` in `/backend`:

```
DATABASE_URL=postgresql://user:pass@host:port/db
GCP_BUCKET_NAME=your-bucket
JWT_SECRET=your-secret
JWT_ALGORITHM=HS256
```

---

## ▶️ How to Run Locally  

### Backend  
```
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend  
```
cd frontend
npm install
npm start
```

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

## 📌 Future Enhancements  
- Role-based access control  
- Email notifications  
- AI-powered report insights  
- Additional file formats  
- Multi‑file parallel processing  

---

## 📄 License  
MIT License

---

## 🤝 Contributions  
PRs and improvements are welcome!

---

## ⭐ Acknowledgment  
This project is a modern cloud implementation inspired by the typical **mainframe → reporting → SharePoint** workflow used in enterprise environments, redesigned using modern engineering practices for learning and demonstration.

------------------------------------------------------------
