#!/bin/bash

# LMNP SAAS - Script d'installation automatique
# Usage: ./scripts/setup.sh

set -e

echo "🚀 Installation de LMNP SAAS..."

# Vérification des prérequis
echo "📋 Vérification des prérequis..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js n'est pas installé"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ npm n'est pas installé"
    exit 1
fi

echo "✅ Prérequis validés"

# Installation Backend
echo "🔧 Installation du backend..."
cd backend

# Création de l'environnement virtuel
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Environnement virtuel créé"
fi

# Activation de l'environnement virtuel
source venv/bin/activate

# Installation des dépendances
pip install -r requirements.txt
echo "✅ Dépendances backend installées"

# Configuration
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "⚠️  Fichier .env créé - Veuillez le configurer avec vos clés API"
fi

cd ..

# Installation Frontend
echo "🎨 Installation du frontend..."
cd frontend

# Installation des dépendances
npm install
echo "✅ Dépendances frontend installées"

# Configuration
if [ ! -f ".env.local" ]; then
    cp .env.example .env.local
    echo "✅ Configuration frontend créée"
fi

cd ..

echo "🎉 Installation terminée !"
echo ""
echo "📝 Prochaines étapes :"
echo "1. Configurer backend/.env avec votre clé OpenAI"
echo "2. Lancer le backend : cd backend && source venv/bin/activate && python src/main.py"
echo "3. Lancer le frontend : cd frontend && npm run dev"
echo ""
echo "🌐 L'application sera accessible sur http://localhost:5173"

