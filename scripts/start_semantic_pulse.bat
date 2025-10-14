@echo off
echo ========================================
echo NETTOYAGE ET DEMARRAGE SEMANTIC PULSE X
echo ========================================

echo.
echo 1. Nettoyage des processus Python...
taskkill /F /IM python.exe 2>nul
if %errorlevel% equ 0 (
    echo OK - Processus Python arretes
) else (
    echo INFO - Aucun processus Python en cours
)

echo.
echo 2. Nettoyage des processus Streamlit...
taskkill /F /IM streamlit.exe 2>nul
if %errorlevel% equ 0 (
    echo OK - Processus Streamlit arretes
) else (
    echo INFO - Aucun processus Streamlit en cours
)

echo.
echo 3. Vérification des ports...
for %%P in (8000 8501) do (
  netstat -ano | findstr :%%P >nul
  if %errorlevel% equ 0 (
      echo ATTENTION - Port %%P encore occupe, nettoyage force...
      for /f "tokens=5" %%a in ('netstat -ano ^| findstr :%%P') do taskkill /F /PID %%a 2>nul
  )
)

echo.
echo 4. Attente de libération des ports...
timeout /t 2 /nobreak >nul

echo.
echo 5. Detection environnement virtuel (facultatif)...
set "VENV_ACTIVATE=.venv\Scripts\activate.bat"
if exist %VENV_ACTIVATE% (
  echo Activation .venv detectee
) else (
  echo INFO - Pas de .venv detecte, utilisation de l'environnement courant
)

echo.
echo 6. Changement vers le repertoire racine...
cd /d "%~dp0.."
echo Repertoire courant: %CD%

echo.
echo 7. Démarrage de l'application...
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:8501
echo.

echo Démarrage du backend...
if exist %VENV_ACTIVATE% (
  start "Backend API" cmd /k "cd /d %CD% && call %VENV_ACTIVATE% && python -m uvicorn app.backend.main:app --host 0.0.0.0 --port 8000"
) else (
  start "Backend API" cmd /k "cd /d %CD% && python -m uvicorn app.backend.main:app --host 0.0.0.0 --port 8000"
)

echo Démarrage du frontend...
if exist %VENV_ACTIVATE% (
  start "Frontend Streamlit" cmd /k "cd /d %CD% && call %VENV_ACTIVATE% && streamlit run app/frontend/streamlit_app.py --server.port 8501"
) else (
  start "Frontend Streamlit" cmd /k "cd /d %CD% && streamlit run app/frontend/streamlit_app.py --server.port 8501"
)

echo.
echo Services demarres !
echo Frontend: http://localhost:8501
echo API: http://localhost:8000
echo.
echo Les services sont démarrés dans des fenêtres séparées.
echo Vous pouvez fermer cette fenêtre.
echo.
timeout /t 2 /nobreak >nul


