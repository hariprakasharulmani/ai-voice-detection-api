# ⚡ Quick Start - 5 Minutes to Running API

## 🎯 The Fastest Way to Get Started

### Step 1: Open PowerShell in Project Folder
```powershell
cd "C:\Users\HARI\OneDrive\Desktop\cur"
```

### Step 2: Run These Commands (Copy-Paste One by One)

```powershell
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install everything
pip install -r requirements.txt
```

### Step 3: Create .env File

Create a file named `.env` with this content:
```
API_KEY=my-secret-key-12345
DEBUG=False
```

### Step 4: Start Server
```powershell
python main.py
```

### Step 5: Open Browser
Go to: **http://localhost:8000/docs**

**Done! 🎉**

---

## 📋 What Each File Does (Simple Explanation)

| File | What It Does |
|------|-------------|
| `app/main.py` | The main server - handles requests |
| `app/middleware/auth.py` | Security - checks if API key is correct |
| `app/services/audio_downloader.py` | Downloads audio from internet |
| `app/services/audio_preprocessor.py` | Prepares audio for AI |
| `app/services/inference_service.py` | The AI brain (currently placeholder) |
| `config/settings.py` | All settings and configuration |

---

## 🧪 Test It Works

1. Server running? ✅ (You see "Uvicorn running on http://0.0.0.0:8000")
2. Open: http://localhost:8000/health
3. Should see: `{"status": "healthy", "version": "1.0.0"}`

---

## 📖 Need More Details?

Read **BEGINNER_GUIDE.md** for detailed explanations!
