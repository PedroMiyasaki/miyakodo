@echo off
echo ========================================
echo Thread Cards Template - Local Server
echo ========================================
echo.
echo Starting local server on port 8000 from the project root...
echo.
echo Open: http://localhost:8000/templates/twitter-print/
echo.
echo Press Ctrl+C to stop the server.
echo ========================================
echo.

cd /d "%~dp0..\.."
python -m http.server 8000

pause
