# Virtual Environment Quick Reference

## ✅ Setup Complete!

Your virtual environment has been created and all dependencies are installed.

## How to Use the Virtual Environment

### Activate the Virtual Environment

**Windows Command Prompt:**
```cmd
venv\Scripts\activate
```

**Windows PowerShell:**
```powershell
venv\Scripts\Activate.ps1
```

**Note:** If you get an execution policy error in PowerShell, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Deactivate the Virtual Environment

When you're done working, deactivate it:
```cmd
deactivate
```

## Running the Application

**Always activate the venv first**, then run:

```cmd
# Activate venv
venv\Scripts\activate

# Run the FastAPI server
uvicorn app.main:app --reload
```

Or use the Python executable directly:
```cmd
venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

## Installing New Packages

When you need to install additional packages:

```cmd
# Activate venv first
venv\Scripts\activate

# Install package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt
```

## Why Use a Virtual Environment?

- ✅ **Isolation**: Keeps project dependencies separate from your system Python
- ✅ **Reproducibility**: Ensures consistent environments across different machines
- ✅ **Clean**: Easy to delete and recreate if something goes wrong
- ✅ **Best Practice**: Standard practice in Python development

## Project Structure

```
Claims-Reporting-Automation-System/
├── venv/                    # Virtual environment (don't commit this)
├── app/                     # Your application code
├── requirements.txt         # Project dependencies
├── .env                     # Environment variables (create this)
└── .env.example            # Template for .env file
```

## Next Steps

1. ✅ Virtual environment created
2. ✅ Dependencies installed
3. ⏭️ Create `.env` file with your configuration
4. ⏭️ Set up GCP authentication
5. ⏭️ Run the application!
