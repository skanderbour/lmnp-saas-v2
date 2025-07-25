# Guide de Déploiement LMNP SAAS

Ce guide explique comment déployer LMNP SAAS en production.

## 🌐 Application Déployée

**URL de production actuelle :** https://60h5imcyq9l8.manus.space

## 🚀 Options de déploiement

### 1. Déploiement Full-Stack Intégré (Recommandé)

L'application est configurée pour servir le frontend depuis le backend Flask.

#### Préparation

```bash
# 1. Build du frontend
cd frontend
npm run build

# 2. Copie dans le backend
cp -r dist/* ../backend/src/static/

# 3. Déploiement du backend avec frontend intégré
cd ../backend
# Déployer sur votre plateforme (Heroku, Railway, etc.)
```

### 2. Déploiement Séparé

#### Frontend (Vercel, Netlify)

```bash
cd frontend
npm run build
# Déployer le dossier dist/
```

#### Backend (Heroku, Railway, Render)

```bash
cd backend
# Configurer les variables d'environnement
# Déployer l'application Flask
```

## ⚙️ Configuration Production

### Variables d'environnement

```env
# Production
FLASK_ENV=production
SECRET_KEY=your-super-secret-production-key
JWT_SECRET_KEY=your-jwt-production-key

# Base de données PostgreSQL (recommandé)
DATABASE_URL=postgresql://user:password@host:port/database

# OpenAI API
OPENAI_API_KEY=your-openai-api-key
OPENAI_API_BASE=https://api.openai.com/v1

# CORS (domaines autorisés)
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Sécurité
BCRYPT_LOG_ROUNDS=12
RATELIMIT_DEFAULT=50 per hour

# Monitoring
LOG_LEVEL=WARNING
```

### Base de données

#### Migration vers PostgreSQL

```python
# Installer psycopg2
pip install psycopg2-binary

# Mettre à jour DATABASE_URL
DATABASE_URL=postgresql://user:password@host:port/database
```

#### Migrations

```bash
# Créer les tables
python src/main.py
# Les tables sont créées automatiquement au démarrage
```

## 🔐 Sécurité Production

### 1. HTTPS Obligatoire

```python
# Dans main.py, ajouter :
from flask_talisman import Talisman

app = Flask(__name__)
Talisman(app, force_https=True)
```

### 2. Variables d'environnement sécurisées

- Utiliser un gestionnaire de secrets (AWS Secrets Manager, etc.)
- Ne jamais commiter les clés en dur
- Rotation régulière des clés

### 3. Rate Limiting

```python
# Configuration stricte pour la production
RATELIMIT_DEFAULT = "50 per hour"
RATELIMIT_STORAGE_URL = "redis://localhost:6379"
```

### 4. Monitoring

```python
# Logs structurés
import logging
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)
```

## 📊 Performance

### 1. Cache Redis

```bash
# Installer Redis
pip install redis

# Configuration
CACHE_TYPE = "redis"
CACHE_REDIS_URL = "redis://localhost:6379"
```

### 2. CDN pour les assets

- Utiliser un CDN pour les fichiers statiques
- Optimiser les images
- Minifier CSS/JS

### 3. Base de données

```sql
-- Index pour les performances
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_biens_user_id ON biens_immobiliers(user_id);
CREATE INDEX idx_transactions_bien_id ON transactions(bien_id);
```

## 🔍 Monitoring

### 1. Health Checks

L'endpoint `/api/health` fournit le statut de l'application :

```json
{
  "status": "healthy",
  "components": {
    "database": "healthy",
    "agents_ia": "healthy",
    "api": "healthy"
  }
}
```

### 2. Métriques

- Temps de réponse API
- Utilisation des agents IA
- Erreurs et exceptions
- Utilisation de la base de données

### 3. Alertes

Configurer des alertes pour :
- Erreurs 5xx
- Temps de réponse > 2s
- Utilisation CPU/RAM élevée
- Échecs d'authentification

## 🚀 Plateformes de déploiement

### Heroku

```bash
# Procfile
web: cd backend && python src/main.py

# Déploiement
git add .
git commit -m "Deploy to production"
git push heroku main
```

### Railway

```bash
# railway.json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "cd backend && python src/main.py"
  }
}
```

### Render

```yaml
# render.yaml
services:
  - type: web
    name: lmnp-saas
    env: python
    buildCommand: "cd backend && pip install -r requirements.txt"
    startCommand: "cd backend && python src/main.py"
```

### Docker

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Backend
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ ./backend/
COPY frontend/dist/ ./backend/src/static/

EXPOSE 5000

CMD ["python", "backend/src/main.py"]
```

## 🔄 CI/CD

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '18'
          
      - name: Build Frontend
        run: |
          cd frontend
          npm install
          npm run build
          
      - name: Deploy to Production
        run: |
          # Votre script de déploiement
```

## 📋 Checklist de déploiement

### Avant le déploiement

- [ ] Tests passent en local
- [ ] Frontend build sans erreurs
- [ ] Variables d'environnement configurées
- [ ] Base de données prête
- [ ] Domaine configuré
- [ ] SSL/TLS activé

### Après le déploiement

- [ ] Health check OK
- [ ] Interface accessible
- [ ] API fonctionnelle
- [ ] Agents IA opérationnels
- [ ] Logs sans erreurs critiques
- [ ] Performance acceptable

## 🆘 Résolution de problèmes

### Erreurs communes

#### "Application Error"
- Vérifier les logs
- Vérifier les variables d'environnement
- Vérifier la connectivité base de données

#### "CORS Error"
- Vérifier CORS_ORIGINS
- Vérifier le domaine frontend

#### "OpenAI API Error"
- Vérifier la clé API
- Vérifier les crédits OpenAI
- Vérifier les limites de taux

### Logs de débogage

```bash
# Activer les logs détaillés
LOG_LEVEL=DEBUG

# Consulter les logs
heroku logs --tail  # Heroku
railway logs        # Railway
```

## 📈 Scaling

### Horizontal Scaling

- Utiliser un load balancer
- Déployer plusieurs instances
- Base de données partagée

### Vertical Scaling

- Augmenter CPU/RAM
- Optimiser les requêtes
- Cache intelligent

## 🔒 Backup

### Base de données

```bash
# PostgreSQL
pg_dump $DATABASE_URL > backup.sql

# Restauration
psql $DATABASE_URL < backup.sql
```

### Fichiers

- Sauvegarder les uploads utilisateurs
- Sauvegarder la configuration
- Versioning du code

---

**Application en production :** https://60h5imcyq9l8.manus.space

