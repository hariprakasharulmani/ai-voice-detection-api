# 🚀 Beginner-Friendly Step-by-Step Guide

## What We Built

You now have a complete AI Voice Detection API! Here's what each part does:

- **`app/main.py`** - The main API server (like the brain)
- **`app/middleware/auth.py`** - Security guard (checks API keys)
- **`app/services/audio_downloader.py`** - Downloads audio from URLs
- **`app/services/audio_preprocessor.py`** - Prepares audio for AI model
- **`app/services/inference_service.py`** - The AI model (currently placeholder)

---

## Step 1: Install Python (If Not Already Installed)

1. Check if Python is installed:
   ```powershell
   python --version
   ```
   You should see something like `Python 3.10.x` or higher.

2. If not installed, download from: https://www.python.org/downloads/
   - ✅ Check "Add Python to PATH" during installation

---

## Step 2: Open Terminal in Your Project

1. **Option A - Using File Explorer:**
   - Navigate to: `C:\Users\HARI\OneDrive\Desktop\cur`
   - Right-click in the folder → "Open in Terminal" or "Open PowerShell here"

2. **Option B - Using Command:**
   - Press `Win + R`, type `powershell`, press Enter
   - Type: `cd "C:\Users\HARI\OneDrive\Desktop\cur"`

---

## Step 3: Create Virtual Environment (Isolated Python Space)

**Why?** This keeps your project's packages separate from other projects.

```powershell
python -m venv venv
```

**What happened?** A folder called `venv` was created.

---

## Step 4: Activate Virtual Environment

```powershell
venv\Scripts\activate
```

**You'll see `(venv)` at the start of your terminal line** - that means it's active!

**If you see an error**, try:
```powershell
venv\Scripts\Activate.ps1
```

If that fails, you may need to allow scripts:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Step 5: Install All Required Packages

```powershell
pip install -r requirements.txt
```

**This will take 2-5 minutes** - it's downloading:
- FastAPI (web framework)
- PyTorch (AI/ML library)
- librosa (audio processing)
- And other dependencies

**Wait for it to finish!** You'll see "Successfully installed..." at the end.

---

## Step 6: Create Environment Configuration File

1. Create a file named `.env` in your project folder
   - You can use Notepad or any text editor

2. Add this content:
   ```env
   API_KEY=my-secret-key-12345
   DEBUG=False
   HOST=0.0.0.0
   PORT=8000
   ```

3. Save the file as `.env` (make sure it's exactly `.env`, not `.env.txt`)

**What is this?** This file stores your secret API key and settings.

---

## Step 7: Test That Everything Works

```powershell
python -c "from app.main import app; print('✅ Success! Everything is installed correctly!')"
```

**If you see ✅ Success!** - You're ready to go!

**If you see an error** - Check Step 5 again, make sure all packages installed.

---

## Step 8: Start the API Server

```powershell
python main.py
```

**You should see:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**🎉 Your API is now running!**

**Keep this terminal window open** - the server needs to keep running.

---

## Step 9: Test the API (Open in Browser)

1. Open your web browser
2. Go to: `http://localhost:8000/docs`
3. You'll see a beautiful API documentation page!

**What you can do here:**
- Click on `/health` → "Try it out" → "Execute" - Should return `{"status": "healthy"}`
- Click on `/detect-voice` to see the API endpoint

---

## Step 10: Test the Voice Detection Endpoint

### Option A: Using the Browser Interface

1. In `http://localhost:8000/docs`
2. Click on `POST /detect-voice`
3. Click "Try it out"
4. Click "Authorize" button at top
   - Enter: `my-secret-key-12345` (your API key from `.env`)
5. In the request body, paste:
   ```json
   {
     "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
     "language": "en"
   }
   ```
6. Click "Execute"

**Note:** The current model is a placeholder, so it will return a dummy prediction.

---

## Step 11: Test with cURL (Optional - Advanced)

Open a **NEW terminal window** (keep the server running in the first one):

```powershell
curl -X POST "http://localhost:8000/detect-voice" -H "Authorization: Bearer my-secret-key-12345" -H "Content-Type: application/json" -d "{\"audio_url\": \"https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3\", \"language\": \"en\"}"
```

---

## Understanding the Response

When you call the API, you'll get something like:

```json
{
  "prediction": "HUMAN",
  "confidence": 0.65,
  "language": "en",
  "model_version": "1.0.0",
  "processing_time_ms": 450
}
```

**What each field means:**
- `prediction`: "AI_GENERATED" or "HUMAN"
- `confidence`: How sure the model is (0.0 to 1.0)
- `language`: The language you specified
- `model_version`: Version of the AI model
- `processing_time_ms`: How long it took (milliseconds)

---

## Common Issues & Solutions

### ❌ "ModuleNotFoundError: No module named 'fastapi'"
**Solution:** Go back to Step 5, make sure virtual environment is activated (you see `(venv)`)

### ❌ "Port 8000 is already in use"
**Solution:** Either:
- Close the other program using port 8000, OR
- Change port in `.env` file to `PORT=8001`

### ❌ "401 Unauthorized" error
**Solution:** Make sure you're using the correct API key from your `.env` file

### ❌ Can't create `.env` file
**Solution:** 
- Make sure you're saving as "All Files" type
- Or use: `New-Item -Path .env -ItemType File` in PowerShell
- Then edit it with: `notepad .env`

---

## What's Next?

### Current Status:
✅ API structure is complete
✅ Authentication works
✅ Audio download works
✅ Audio preprocessing works
⚠️ **AI Model is placeholder** - needs real model integration

### To Make It Production-Ready:

1. **Choose an AI Model** (we discussed this earlier)
   - Options: ASVspoof, Wav2Vec2, or custom model
   - I can help integrate it once you choose

2. **Update `app/services/inference_service.py`**
   - Replace placeholder with real model loading
   - Add actual inference logic

3. **Deploy to Production**
   - Use cloud services (AWS, Azure, Google Cloud)
   - Or use Docker containers

---

## Quick Reference Commands

```powershell
# Activate virtual environment
venv\Scripts\activate

# Install packages
pip install -r requirements.txt

# Run server
python main.py

# Test import
python -c "from app.main import app; print('OK')"
```

---

## Need Help?

If you get stuck at any step:
1. Check the error message carefully
2. Make sure you're in the right directory
3. Make sure virtual environment is activated
4. Check that all packages installed successfully

**You're doing great! 🎉**
