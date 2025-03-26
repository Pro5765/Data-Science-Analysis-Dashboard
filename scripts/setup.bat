@echo off
echo E-commerce Analytics Dashboard Setup
echo Created by: Vijeta Thakur (2025)
echo =====================================

echo Creating Python virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing required packages...
python -m pip install --upgrade pip

:: Install packages one by one to handle errors better
echo Installing Dash...
pip install dash==2.14.2

echo Installing Pandas...
pip install pandas==2.2.3

echo Installing Plotly...
pip install plotly==5.18.0

echo Installing Kaleido...
pip install kaleido==0.2.1

echo Installing python-docx...
pip install python-docx==1.0.1

echo Installing reportlab...
pip install reportlab==4.0.8

echo.
echo Setup complete! Run start.bat to launch the dashboard.
echo Created by: Vijeta Thakur
