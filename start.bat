@echo off
REM Ce script installe les dépendances et lance l'assistant vocal.

REM Titre de la fenêtre
TITLE Assistant Vocal Local

REM Vérifie si Python est installé et disponible dans le PATH
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Erreur : Python n'est pas installé ou n'est pas dans le PATH.
    echo Veuillez l'installer depuis python.org et vous assurer de cocher "Add Python to PATH".
    pause
    exit /b
)

REM Vérifie si pip est disponible
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Erreur : pip n'est pas disponible. Impossible d'installer les dépendances.
    pause
    exit /b
)

REM Installe les dépendances listées dans requirements.txt
echo Verification et installation des dependances...
pip install -r requirements.txt

REM Lance le script principal de l'assistant
echo Lancement de l'assistant vocal...
python vocal_assistant.py

REM Garde la fenêtre ouverte à la fin pour voir les messages d'erreur
echo.
echo Le script s'est termine. Appuyez sur une touche pour fermer cette fenetre.
pause