@echo off
setlocal

echo Checking for Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in your PATH.
    echo Please install Python 3.10.9 as per the README.
    pause
    exit /b 1
)

echo Creating virtual environment 'venv'...
if not exist "venv" (
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies from requirements.txt...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo Downloading required NLTK data...
python -c "import nltk; nltk.download('vader_lexicon')"

echo Creating output and log folders...
if not exist "output" mkdir output
if not exist "log" mkdir log

echo.
echo Environment setup is complete.
echo To activate this environment in the future, run: venv\Scripts\activate
echo.
pause