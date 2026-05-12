@echo off
chcp 65001 >nul
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
  set PY=py -3
) else (
  set PY=python
)

echo [1/5] Updating OFFICIAL confirmed data from ECDC/WHO/CDC...
%PY% tools\update_official_confirmed.py
if errorlevel 1 (
  echo Official update failed.
  pause
  exit /b 1
)

echo [2/5] Updating ArcGIS signal layer...
if exist tools\update_arcgis_signal.py (
  %PY% tools\update_arcgis_signal.py
) else (
  echo ArcGIS updater not found, skipping signal layer.
)

echo [3/5] Building site data...
%PY% tools\build_site_data.py
if errorlevel 1 (
  echo Build failed.
  pause
  exit /b 1
)

echo [4/5] Validating...
%PY% tools\validate_data.py
if errorlevel 1 (
  echo Validation failed.
  pause
  exit /b 1
)

echo [5/5] Starting local server...
echo Open: http://127.0.0.1:8000
start "" "http://127.0.0.1:8000"
%PY% -m http.server 8000

pause