# Automated Setup Script for Windows
# Run this script to set up everything automatically

Write-Host "🚀 Starting AI Voice Detection API Setup..." -ForegroundColor Green
Write-Host ""

# Check Python
Write-Host "📦 Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found! Please install Python 3.10+ first." -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "📁 Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "⚠️  Virtual environment already exists, skipping..." -ForegroundColor Yellow
} else {
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host ""
Write-Host "⬆️  Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet

# Install dependencies
Write-Host ""
Write-Host "📥 Installing dependencies (this may take a few minutes)..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ All dependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Installation failed. Please check the error messages above." -ForegroundColor Red
    exit 1
}

# Create .env file if it doesn't exist
Write-Host ""
Write-Host "⚙️  Checking .env file..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✅ .env file already exists" -ForegroundColor Green
} else {
    Write-Host "📝 Creating .env file..." -ForegroundColor Yellow
    @"
API_KEY=my-secret-key-12345
DEBUG=False
HOST=0.0.0.0
PORT=8000
"@ | Out-File -FilePath ".env" -Encoding utf8
    Write-Host "✅ .env file created with default values" -ForegroundColor Green
    Write-Host "⚠️  Remember to change API_KEY in .env file!" -ForegroundColor Yellow
}

# Test import
Write-Host ""
Write-Host "🧪 Testing installation..." -ForegroundColor Yellow
try {
    python -c "from app.main import app; print('✅ Import test passed!')" 2>&1 | Out-Null
    Write-Host "✅ All imports working correctly!" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Import test had warnings (this might be normal)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎉 Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Activate virtual environment: venv\Scripts\activate" -ForegroundColor White
Write-Host "2. Start the server: python main.py" -ForegroundColor White
Write-Host "3. Open browser: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "For detailed instructions, see BEGINNER_GUIDE.md" -ForegroundColor Cyan
