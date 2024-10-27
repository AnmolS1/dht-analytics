@echo off

REM Check if pip is installed
where pip >nul 2>nul
if %errorlevel% neq 0 (
	echo pip could not be found. Please install Python and pip.
	exit /b 1
)

REM Install required packages
pip install -r requirements.txt

echo All dependencies have been installed successfully.