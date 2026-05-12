@echo off
chcp 65001 >nul
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
  set PY=py -3
) else (
  set PY=python
)

%PY% tools\build_site_data.py
%PY% tools\validate_data.py
start "" "http://127.0.0.1:8000"
%PY% -m http.server 8000
pause
