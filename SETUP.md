# Quick Setup Guide

## The Error You're Seeing

If you see errors like:
- `ModuleNotFoundError: No module named 'fastapi'`
- Import warnings in your IDE

**This is normal!** The dependencies haven't been installed yet.

## Fix the Error - Install Dependencies

1. **Open terminal in the project directory:**
   ```powershell
   cd c:\Users\HARI\OneDrive\Desktop\cur
   ```

2. **Create virtual environment (recommended):**
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install all dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Create `.env` file** (copy from `.env.example` if it exists, or create manually):
   ```env
   API_KEY=your-secret-api-key-here
   DEBUG=False
   HOST=0.0.0.0
   PORT=8000
   ```

5. **Test the installation:**
   ```powershell
   python -c "from app.main import app; print('✓ All imports successful!')"
   ```

6. **Run the API:**
   ```powershell
   python main.py
   ```

The API will start at `http://localhost:8000`

## Verify Installation

After installing, the errors should disappear. You can verify by:
- Running the import test above
- Starting the server
- Visiting `http://localhost:8000/docs` for the API documentation
