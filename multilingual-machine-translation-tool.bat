@echo off

if exist "%~dp0\pyvenv.cfg" (
    echo Virtual environment already exists
) else (
    echo Creating virtual environment...
    python -m venv "%CD%"
    echo Activating virtual environment...
    call "%CD%\Scripts\activate.bat"
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Activer l'environnement virtuel
call "%~dp0Scripts\activate.bat"

REM Lancer le script Python
python translator/main.py

REM Désactiver l'environnement virtuel après exécution
deactivate

REM Empêcher la fermeture automatique de la fenêtre
pause