# Guide d'Installation LMNP SAAS

Ce guide vous accompagne pas à pas pour installer et configurer LMNP SAAS sur votre machine locale.

## 📋 Prérequis

Avant de commencer, assurez-vous d'avoir installé :

### Obligatoire
- **Python 3.11+** - [Télécharger Python](https://www.python.org/downloads/)
- **Node.js 18+** - [Télécharger Node.js](https://nodejs.org/)
- **Git** - [Télécharger Git](https://git-scm.com/)

### Recommandé
- **VS Code** - [Télécharger VS Code](https://code.visualstudio.com/)
- **Postman** - Pour tester l'API

### Vérification des prérequis

```bash
# Vérifier Python
python --version
# ou
python3 --version

# Vérifier Node.js
node --version

# Vérifier npm
npm --version

# Vérifier Git
git --version
```

## 🚀 Installation Rapide

### Option 1 : Script automatique (Recommandé)

#### Linux/macOS
```bash
git clone https://github.com/votre-username/lmnp-saas.git
cd lmnp-saas
./scripts/setup.sh
```

#### Windows
```cmd
git clone https://github.com/votre-username/lmnp-saas.git
cd lmnp-saas
scripts\setup.bat
```

### Option 2 : Installation manuelle

Si vous préférez contrôler chaque étape :

#### 1. Cloner le projet
```bash
git clone https://github.com/votre-username/lmnp-saas.git
cd lmnp-saas
```

#### 2. Backend (API Flask)

```bash
cd backend

# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
```

#### 3. Frontend (Interface React)

```bash
cd ../frontend

# Installer les dépendances
npm install

# Configurer les variables d'environnement
cp .env.example .env.local
```

## ⚙️ Configuration

### 1. Configuration Backend (.env)

Éditez le fichier `backend/.env` :

```env
# OBLIGATOIRE : Clé OpenAI pour les agents IA
OPENAI_API_KEY=sk-your-openai-api-key-here

# Optionnel : Base OpenAI (par défaut : https://api.openai.com/v1)
OPENAI_API_BASE=https://api.openai.com/v1

# Configuration Flask
FLASK_ENV=development
SECRET_KEY=your-secret-key-minimum-32-characters
JWT_SECRET_KEY=your-jwt-secret-key

# Base de données (SQLite par défaut)
DATABASE_URL=sqlite:///lmnp_saas.db

# CORS pour le développement
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 2. Configuration Frontend (.env.local)

Éditez le fichier `frontend/.env.local` :

```env
# URL de l'API backend
VITE_API_URL=http://localhost:5000/api

# Configuration optionnelle
VITE_APP_NAME=LMNP Expert
VITE_DEBUG=true
```

### 3. Obtenir une clé OpenAI

1. Créez un compte sur [OpenAI](https://platform.openai.com/)
2. Allez dans [API Keys](https://platform.openai.com/api-keys)
3. Créez une nouvelle clé API
4. Copiez la clé dans votre fichier `.env`

⚠️ **Important** : Gardez votre clé API secrète et ne la commitez jamais dans Git.

## 🏃‍♂️ Lancement de l'application

### 1. Démarrer le Backend

```bash
cd backend

# Activer l'environnement virtuel
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows

# Lancer le serveur
python src/main.py
```

Le backend sera accessible sur : **http://localhost:5000**

### 2. Démarrer le Frontend

Dans un nouveau terminal :

```bash
cd frontend

# Lancer le serveur de développement
npm run dev
```

Le frontend sera accessible sur : **http://localhost:5173**

## 🧪 Vérification de l'installation

### 1. Tester l'API Backend

Ouvrez votre navigateur et allez sur :
- http://localhost:5000/api/health
- http://localhost:5000/api/docs

Vous devriez voir des réponses JSON.

### 2. Tester l'Interface Frontend

Ouvrez votre navigateur et allez sur :
- http://localhost:5173

Vous devriez voir l'interface LMNP Expert.

### 3. Tester les Agents IA

Dans l'interface, essayez de :
1. Créer un utilisateur
2. Ajouter un bien immobilier
3. Faire un calcul fiscal
4. Utiliser le chat avec les agents IA

## 🐛 Résolution des problèmes

### Problème : "Module not found"

**Solution** : Vérifiez que l'environnement virtuel est activé et que les dépendances sont installées.

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Problème : "CORS error"

**Solution** : Vérifiez que l'URL du frontend est dans `CORS_ORIGINS` du backend.

### Problème : "OpenAI API error"

**Solution** : Vérifiez que votre clé OpenAI est correcte et que vous avez des crédits.

### Problème : "Port already in use"

**Solution** : Changez le port ou arrêtez le processus qui l'utilise.

```bash
# Trouver le processus
lsof -i :5000  # Linux/macOS
netstat -ano | findstr :5000  # Windows

# Arrêter le processus
kill -9 PID  # Linux/macOS
taskkill /PID PID /F  # Windows
```

### Problème : Base de données

**Solution** : Supprimez le fichier de base de données et relancez.

```bash
rm backend/src/database/app.db
python backend/src/main.py
```

## 🔧 Développement

### Structure des logs

Les logs sont affichés dans la console :
- **Backend** : Logs Flask dans le terminal backend
- **Frontend** : Logs dans la console du navigateur (F12)

### Base de données

La base de données SQLite est créée automatiquement dans :
`backend/src/database/app.db`

Pour l'inspecter :
```bash
cd backend/src/database
sqlite3 app.db
.tables
.schema users
SELECT * FROM users;
```

### Tests

```bash
# Tests backend
cd backend
python -m pytest tests/ -v

# Tests frontend
cd frontend
npm run test
```

## 📚 Ressources

- [Documentation API](docs/api/)
- [Guide utilisateur](docs/user/)
- [Documentation technique](docs/technical/)
- [Rapport de livraison](docs/rapport_livraison_final_lmnp_saas.md)

## 🆘 Support

Si vous rencontrez des problèmes :

1. Vérifiez ce guide de résolution des problèmes
2. Consultez les logs d'erreur
3. Vérifiez les issues GitHub
4. Contactez le support : support@lmnp-saas.com

## 🎯 Prochaines étapes

Une fois l'installation réussie :

1. **Explorez l'interface** - Familiarisez-vous avec les fonctionnalités
2. **Testez les agents IA** - Essayez les différents agents spécialisés
3. **Importez des données** - Ajoutez vos biens et transactions
4. **Personnalisez** - Adaptez l'interface à vos besoins
5. **Développez** - Ajoutez vos propres fonctionnalités

Bon développement ! 🚀

