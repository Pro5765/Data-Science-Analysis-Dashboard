@echo off
echo E-commerce Analytics Dashboard
echo Created by: Vijeta Thakur (2025)
echo ============================

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Set environment variables
set PYTHONPATH=%~dp0..

:: Change to project root directory
cd %~dp0..

:: Start the dashboard
echo Starting the dashboard...
echo Created by: Vijeta Thakur
echo Visit http://localhost:8050 in your browser
echo.

python src/dashboard/app.py

echo.
echo Dashboard stopped. Press any key to exit.
echo Created by: Vijeta Thakur
pause
