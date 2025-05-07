@echo off

set INSTALLATIONLOGS=Installation.log
set ERRORLOGS=Error.log

echo ----- > %INSTALLATIONLOGS%

if exist "%CD%\pyvenv.cfg" (
    echo Virtual environment already exists :D
    echo May take a while to load...
) else (
    echo Instalation logs will be saved in %INSTALLATIONLOGS%
    echo Creating virtual environment...
    python -m venv "%CD%" >> %INSTALLATIONLOGS% 2>&1
    echo Activating virtual environment...
    call "%CD%\Scripts\activate.bat"
    echo Installing dependencies, may take some times...
    echo Installation of 2Gb packages. sorry (ㅠ﹏ㅠ)
    timeout /t 10 /nobreak > nul
    pip install -r requirements.txt >> %INSTALLATIONLOGS% 2>&1
)

REM Activer l'environnement virtuel
call "%~dp0Scripts\activate.bat"

REM Lancer le script Python avec redirection des erreurs
python translator/main.py
pause


REM Désactiver l'environnement virtuel après exécution
deactivate