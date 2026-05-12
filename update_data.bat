@echo off
chcp 65001 >nul
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
  set PY=py -3
) else (
  set PY=python
)

%PY% tools\update_official_confirmed.py
if exist tools\update_arcgis_signal.py %PY% tools\update_arcgis_signal.py
%PY% tools\build_site_data.py
%PY% tools\validate_data.py

pause