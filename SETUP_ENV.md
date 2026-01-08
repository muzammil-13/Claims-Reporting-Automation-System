# Environment Variables Setup Guide

This guide explains how to set up environment variables for the Claims Reporting Automation System on Windows.

## Method 1: Using .env File (Recommended for Local Development)

### Step 1: Create .env file

1. Copy the `.env.example` file to `.env`:

   ```cmd
   copy .env.example .env
   ```
2. Edit `.env` with your actual values:

   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/claims_db
   GCP_BUCKET_NAME=your-actual-bucket-name
   ```

### Step 2: Install python-dotenv

The project already includes `python-dotenv` in requirements.txt. Install it:

```cmd
pip install -r requirements.txt
```

The code will automatically load variables from `.env` when the application starts.

---

## Method 2: Set Windows Environment Var iables (Permanent)

### Option A: Using System Properties (GUI)

1. Press `Win + X` and select **System**
2. Click **Advanced system settings**
3. Click **Environment Variables**
4. Under **User variables**, click **New**
5. Add each variable:
   - Variable name: `DATABASE_URL`
   - Variable value: `postgresql://user:password@localhost:5432/claims_db`
6. Repeat for `GCP_BUCKET_NAME`

### Option B: Using Command Prompt (Temporary - Current Session Only)

```cmd
set DATABASE_URL=postgresql://user:password@localhost:5432/claims_db
set GCP_BUCKET_NAME=your-bucket-name
```

### Option C: Using PowerShell (Temporary - Current Session Only)

```powershell
$env:DATABASE_URL="postgresql://user:password@localhost:5432/claims_db"
$env:GCP_BUCKET_NAME="your-bucket-name"
```

### Option D: Using PowerShell (Permanent - User Level)

```powershell
[System.Environment]::SetEnvironmentVariable('DATABASE_URL', 'postgresql://user:password@localhost:5432/claims_db', 'User')
[System.Environment]::SetEnvironmentVariable('GCP_BUCKET_NAME', 'your-bucket-name', 'User')
```

**Note:** After setting permanent variables, restart your terminal/IDE for changes to take effect.

---

## Google Cloud Storage Authentication Setup

The application uses **Application Default Credentials (ADC)** to authenticate with Google Cloud Storage. Here are the setup options:

### Option 1: Using gcloud CLI (Recommended for Local Development)

1. **Install Google Cloud SDK** (if not already installed):

   - Download from: https://cloud.google.com/sdk/docs/install
   - Or use: `winget install Google.CloudSDK`
2. **Authenticate with your Google account**:

   ```cmd
   gcloud auth login
   ```
3. **Set your project**:

   ```cmd
   gcloud config set project YOUR_PROJECT_ID
   ```
4. **Set Application Default Credentials**:

   ```cmd
   gcloud auth application-default login
   ```

   This will open a browser window for authentication. After completing, credentials are stored locally.
5. **Verify authentication**:

   ```cmd
   gcloud auth application-default print-access-token
   ```

### Option 2: Using Service Account Key File

1. **Create a service account** in Google Cloud Console:

   - Go to **IAM & Admin** → **Service Accounts**
   - Click **Create Service Account**
   - Grant it **Storage Admin** role
   - Create and download a JSON key
2. **Set the environment variable**:

   ```cmd
   set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\your\service-account-key.json
   ```

   Or add to `.env` file:

   ```
   GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\your\service-account-key.json
   ```

### Option 3: Using Service Account in .env (Alternative)

If you prefer to specify the key path in `.env`:

```
GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\service-account-key.json
```

---

## Database Setup

### PostgreSQL (Production-like)

1. **Install PostgreSQL** (if not installed):

   - Download from: https://www.postgresql.org/download/windows/
   - Or use: `winget install PostgreSQL.PostgreSQL`
2. **Create database**:

   ```cmd
   psql -U postgres
   CREATE DATABASE claims_db;
   ```
3. **Set DATABASE_URL**:

   ```
   DATABASE_URL=postgresql://postgres:your_password@localhost:5432/claims_db
   ```

### SQLite (Default - No Setup Required)

If `DATABASE_URL` is not set, the app defaults to SQLite:

- Database file: `claims.db` (created automatically in project root)
- No additional setup needed!

---

## Quick Start Checklist

- [ ] Copy `.env.example` to `.env`
- [ ] Edit `.env` with your values
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Set up GCP authentication (choose one):
  - [ ] `gcloud auth application-default login` (recommended)
  - [ ] Set `GOOGLE_APPLICATION_CREDENTIALS` environment variable
- [ ] Create GCS bucket (if needed):
  ```cmd
  gsutil mb gs://your-bucket-name
  ```
- [ ] Set up database (PostgreSQL or use default SQLite)
- [ ] Run the application:
  ```cmd
  uvicorn app.main:app --reload
  ```

---

## Verify Your Setup

Test that environment variables are loaded correctly:

```python
# Run this in Python
import os
from dotenv import load_dotenv
load_dotenv()

print("DATABASE_URL:", os.getenv("DATABASE_URL"))
print("GCP_BUCKET_NAME:", os.getenv("GCP_BUCKET_NAME"))
```

---

## Troubleshooting

### "GCP_BUCKET_NAME is not configured"

- Make sure you've set `GCP_BUCKET_NAME` in `.env` or as an environment variable
- Restart your terminal/IDE after setting environment variables

### "Application Default Credentials not found"

- Run: `gcloud auth application-default login`
- Or set `GOOGLE_APPLICATION_CREDENTIALS` to point to your service account key

### "Permission denied" when accessing GCS

- Ensure your service account/user has **Storage Admin** or **Storage Object Admin** role
- Check bucket permissions in Google Cloud Console

### Database connection errors

- Verify PostgreSQL is running: `pg_isready`
- Check connection string format: `postgresql://user:pass@host:port/dbname`
- For SQLite, ensure the directory is writable
