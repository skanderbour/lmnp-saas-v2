#!/bin/bash

echo "🚀 Démarrage LMNP SAAS v2.0"
echo "=========================="

# Vérification des prérequis
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 requis"
    exit 1
fi

if ! command -v pnpm &> /dev/null; then
    echo "❌ pnpm requis"
    exit 1
fi

# Démarrage du backend
echo "📊 Démarrage du backend Flask..."
cd backend
source venv/bin/activate
python src/main.py &
BACKEND_PID=$!
echo "✅ Backend démarré (PID: $BACKEND_PID)"

# Attendre que le backend soit prêt
sleep 3

# Démarrage du frontend
echo "🌐 Démarrage du frontend React..."
cd ../frontend
pnpm run dev --host &
FRONTEND_PID=$!
echo "✅ Frontend démarré (PID: $FRONTEND_PID)"

echo ""
echo "🎉 Application LMNP SAAS v2.0 démarrée !"
echo "📱 Frontend: http://localhost:5174"
echo "🔧 Backend:  http://localhost:5000"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter l'application"

# Fonction de nettoyage
cleanup() {
    echo ""
    echo "🛑 Arrêt de l'application..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Application arrêtée"
    exit 0
}

# Capture du signal d'interruption
trap cleanup SIGINT

# Attendre indéfiniment
wait
