@echo off
REM LMNP SAAS - Script d'installation automatique pour Windows
REM Usage: scripts\setup.bat

echo 🚀 Installation de LMNP SAAS...

REM Vérification des prérequis
echo 📋 Vérification des prérequis...

python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé
    pause
    exit /b 1
)

node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js n'est pas installé
    pause
    exit /b 1
)

npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ npm n'est pas installé
    pause
    exit /b 1
)

echo ✅ Prérequis validés

REM Installation Backend
echo 🔧 Installation du backend...
cd backend

REM Création de l'environnement virtuel
if not exist "venv" (
    python -m venv venv
    echo ✅ Environnement virtuel créé
)

REM Activation de l'environnement virtuel
call venv\Scripts\activate

REM Installation des dépendances
pip install -r requirements.txt
echo ✅ Dépendances backend installées

REM Configuration
if not exist ".env" (
    copy .env.example .env
    echo ⚠️  Fichier .env créé - Veuillez le configurer avec vos clés API
)

cd ..

REM Installation Frontend
echo 🎨 Installation du frontend...
cd frontend

REM Installation des dépendances
npm install
echo ✅ Dépendances frontend installées

REM Configuration
if not exist ".env.local" (
    copy .env.example .env.local
    echo ✅ Configuration frontend créée
)

cd ..

echo 🎉 Installation terminée !
echo.
echo 📝 Prochaines étapes :
echo 1. Configurer backend\.env avec votre clé OpenAI
echo 2. Lancer le backend : cd backend ^&^& venv\Scripts\activate ^&^& python src\main.py
echo 3. Lancer le frontend : cd frontend ^&^& npm run dev
echo.
echo 🌐 L'application sera accessible sur http://localhost:5173
pause

