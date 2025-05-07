@echo off

REM Désinstaller Argos Translate
echo Uninstalling Argos Translate...
pip uninstall -y argostranslate

REM Supprimer les fichiers temporaires d'Argos Translate
echo Deleting temporary files created by Argos Translate...
set TEMP_FOLDER=%TEMP%\argos-translate
if exist "%TEMP_FOLDER%" (
    rmdir /s /q "%TEMP_FOLDER%"
    echo Temporary files deleted.
) else (
    echo No temporary files found.
)

REM Supprimer le dossier du projet
echo Deleting the project folder...
cd ..
set PROJECT_FOLDER=%~dp0
rmdir /s /q "%PROJECT_FOLDER%"
echo Project folder deleted.

REM Confirmation de la désinstallation
echo Uninstallation complete.
pause