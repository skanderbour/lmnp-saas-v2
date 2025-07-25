# Architecture Backend - LMNP SAAS

Ce document détaille l'architecture du backend de l'application LMNP SAAS.




## 1. Vue d'ensemble de l'architecture

Le backend de l'application LMNP SAAS est construit avec le micro-framework **Flask** en Python. Il suit une architecture modulaire pour séparer les préoccupations et faciliter la maintenance et l'évolution future.

Les composants principaux sont :

- **Application Factory (`create_app` dans `main.py`)**: Le point d'entrée qui configure et assemble toutes les parties de l'application.
- **Blueprints**: Pour organiser les routes en groupes logiques (par exemple, `lmnp` pour la gestion des données et `agents` pour les fonctionnalités IA).
- **SQLAlchemy ORM**: Pour interagir avec la base de données SQLite de manière orientée objet.
- **Services**: Pour encapsuler la logique métier complexe, comme les calculs fiscaux et l'interaction avec les modèles de langage.

---

## 2. Structure des Fichiers et Dossiers

Le backend est organisé comme suit :

```
backend/
├── venv/                  # Environnement virtuel Python
├── .env.example           # Modèle pour les variables d'environnement
├── .env                   # Fichier de configuration (local)
├── requirements.txt       # Dépendances Python
└── src/
    ├── __init__.py        # Initialisation du package
    ├── main.py            # Point d'entrée de l'application Flask
    ├── database_config.py # Configuration de la base de données
    ├── models/            # Modèles de données SQLAlchemy
    │   ├── __init__.py
    │   ├── unified_models.py # Modèles principaux (User, Bien, etc.)
    │   └── ...
    ├── routes/            # Définition des routes de l'API
    │   ├── __init__.py
    │   └── unified_routes.py # Endpoints pour /api/lmnp et /api/agents
    └── services/          # Logique métier
        ├── __init__.py
        ├── expertise_fiscale_lmnp.py # Moteur de calcul fiscal
        └── agents_ia_simple_lmnp.py  # Orchestration des agents IA
```

---

## 3. Point d'Entrée : `main.py`

Le fichier `main.py` est le cœur de l'application. Il est responsable de :

1.  **Création de l'application Flask** via la fonction `create_app()`.
2.  **Configuration de l'application** :
    - **CORS (Cross-Origin Resource Sharing)** : Permet au frontend (servi depuis un autre port) de communiquer avec l'API.
    - **Logging** : Configure un système de journalisation pour suivre les événements et les erreurs.
    - **Secret Key** : Clé secrète pour la gestion des sessions et la sécurité.
3.  **Initialisation de la base de données** en appelant `init_database(app)` depuis `database_config.py`.
4.  **Enregistrement des Blueprints** :
    - `lmnp_bp` est enregistré sous le préfixe `/api/lmnp`.
    - `agents_bp` est enregistré sous le préfixe `/api/agents`.
5.  **Définition des routes de base** :
    - `/api`: Une route d'accueil qui décrit l'API.
    - `/api/health`: Un endpoint de vérification de l'état de santé du service, qui vérifie la connexion à la base de données et la disponibilité des clés API pour les services d'IA.
    - `/api/docs`: Fournit une documentation de base des endpoints disponibles.
6.  **Gestion des erreurs** : Des gestionnaires d'erreurs personnalisés pour les codes 404 (Not Found) et 500 (Internal Server Error) renvoient des réponses JSON claires.
7.  **Service des fichiers statiques** : Une route `/<path:path>` est configurée pour servir les fichiers statiques du frontend React (le `index.html` et les assets associés) lorsque l'application est déployée en production.





---

## 4. Configuration de la Base de Données

### 4.1 Fichier `database_config.py`

Ce fichier centralise la configuration de la base de données SQLAlchemy. Il :

1. **Crée une instance SQLAlchemy unique** (`db`) partagée par tous les modules pour éviter les conflits d'instances.
2. **Définit la fonction `init_database(app)`** qui :
   - Configure l'URI de la base de données SQLite (stockée dans `backend/src/database/app.db`).
   - Désactive le suivi des modifications SQLAlchemy pour améliorer les performances.
   - Initialise l'instance SQLAlchemy avec l'application Flask.
   - Importe tous les modèles et crée les tables automatiquement avec `db.create_all()`.

### 4.2 Base de Données SQLite

L'application utilise **SQLite** comme système de gestion de base de données, ce qui présente plusieurs avantages :
- **Simplicité** : Pas de serveur de base de données séparé à configurer.
- **Portabilité** : Le fichier de base de données peut être facilement sauvegardé et déplacé.
- **Performance** : Suffisant pour les besoins d'une application SAAS de taille moyenne.

Le fichier de base de données est créé automatiquement dans `backend/src/database/app.db` lors du premier lancement.

---

## 5. Modèles de Données (ORM)

L'application utilise **SQLAlchemy ORM** pour interagir avec la base de données. Les modèles sont définis dans `models/unified_models.py` et représentent les entités métier principales.

### 5.1 Modèle `User`

**Table :** `users`

Représente un utilisateur de l'application (propriétaire de biens LMNP).

**Champs principaux :**
- `id` (Integer, PK) : Identifiant unique
- `email` (String, unique) : Adresse email (utilisée pour l'authentification)
- `nom`, `prenom` (String) : Nom et prénom
- `adresse`, `code_postal`, `ville` (String) : Coordonnées
- `telephone` (String) : Numéro de téléphone
- `date_creation` (DateTime) : Date de création du compte
- `actif` (Boolean) : Statut du compte

**Relations :**
- `biens` : Relation One-to-Many vers `BienImmobilier`
- `declarations` : Relation One-to-Many vers `DeclarationFiscale`

### 5.2 Modèle `BienImmobilier`

**Table :** `biens_immobiliers`

Représente un bien immobilier loué en meublé non professionnel.

**Champs principaux :**
- `id` (Integer, PK) : Identifiant unique
- `user_id` (Integer, FK) : Référence vers le propriétaire
- `nom` (String) : Nom du bien (ex: "Appartement Paris 15e")
- `adresse`, `code_postal`, `ville` (String) : Localisation
- `surface` (Float), `nb_pieces` (Integer) : Caractéristiques physiques
- `type_location` (Enum) : Type de location (meublé classé/non classé/autre)
- `regime_fiscal` (Enum) : Régime fiscal choisi (micro-BIC/réel)
- `date_acquisition`, `prix_acquisition` (Date, Numeric) : Informations d'achat
- `valeur_amortissable`, `amortissements_cumules` (Numeric) : Gestion des amortissements

**Relations :**
- `transactions` : Relation One-to-Many vers `Transaction`

### 5.3 Modèle `Transaction`

**Table :** `transactions`

Représente une transaction financière (recette ou charge) liée à un bien.

**Champs principaux :**
- `id` (Integer, PK) : Identifiant unique
- `bien_id` (Integer, FK) : Référence vers le bien concerné
- `date_transaction` (Date) : Date de la transaction
- `libelle` (String) : Description de la transaction
- `montant` (Numeric) : Montant en euros
- `type_transaction` (String) : "recette" ou "charge"
- `categorie`, `sous_categorie` (String) : Catégorisation fiscale
- `compte_comptable` (String) : Numéro de compte comptable
- `source` (String) : Origine de la saisie (manuel, import, OCR)
- `confiance_categorisation` (Float) : Niveau de confiance de l'IA pour la catégorisation

### 5.4 Modèle `DeclarationFiscale`

**Table :** `declarations_fiscales`

Représente une déclaration fiscale annuelle pour un utilisateur.

**Champs principaux :**
- `id` (Integer, PK) : Identifiant unique
- `user_id` (Integer, FK) : Référence vers l'utilisateur
- `annee_fiscale` (Integer) : Année de la déclaration
- `regime_fiscal` (Enum) : Régime fiscal utilisé
- `statut` (String) : État de la déclaration (brouillon/validée/transmise)
- `total_recettes`, `total_charges` (Numeric) : Totaux calculés
- `benefice_brut`, `benefice_net` (Numeric) : Résultats fiscaux
- `amortissements` (Numeric) : Total des amortissements

### 5.5 Modèle `Document`

**Table :** `documents`

Représente un document uploadé par l'utilisateur (factures, contrats, etc.).

**Champs principaux :**
- `id` (Integer, PK) : Identifiant unique
- `user_id` (Integer, FK) : Référence vers l'utilisateur
- `bien_id` (Integer, FK, optionnel) : Référence vers le bien concerné
- `nom_fichier` (String) : Nom original du fichier
- `type_document` (String) : Type (facture, contrat, justificatif)
- `chemin_fichier` (String) : Chemin de stockage sur le serveur
- `contenu_ocr` (Text) : Texte extrait par OCR
- `confiance_ocr` (Float) : Niveau de confiance de l'OCR

### 5.6 Énumérations

**`TypeLocation`** :
- `MEUBLE_CLASSE` : Meublé de tourisme classé
- `MEUBLE_NON_CLASSE` : Meublé de tourisme non classé
- `AUTRE` : Autre type de location meublée

**`RegimeFiscal`** :
- `MICRO_BIC` : Régime micro-BIC (abattement forfaitaire)
- `REEL` : Régime réel (déduction des charges réelles)



---

## 6. Routes API (Endpoints)

L'API est organisée en deux blueprints principaux définis dans `routes/unified_routes.py` :

### 6.1 Blueprint LMNP (`/api/lmnp`)

Ce blueprint gère les données métier principales de l'application.

#### **Gestion des Utilisateurs**

- **`GET /api/lmnp/users`** : Récupère tous les utilisateurs
  - Réponse : `{'users': [...], 'total': int}`

- **`POST /api/lmnp/users`** : Crée un nouvel utilisateur
  - Body : `{'email': string, 'nom': string, 'prenom'?: string, ...}`
  - Réponse : `{'message': string, 'user': {...}}`
  - Validation : Email unique requis

- **`GET /api/lmnp/users/<id>`** : Récupère un utilisateur spécifique
  - Réponse : `{'user': {...}}`

#### **Gestion des Biens Immobiliers**

- **`GET /api/lmnp/biens`** : Récupère tous les biens
  - Paramètre optionnel : `?user_id=int` (filtre par utilisateur)
  - Réponse : `{'biens': [...], 'total': int}`

- **`POST /api/lmnp/biens`** : Crée un nouveau bien immobilier
  - Body : `{'user_id': int, 'nom': string, 'adresse': string, ...}`
  - Validation : Utilisateur existant requis
  - Conversion automatique des types d'énumération

#### **Gestion des Transactions**

- **`GET /api/lmnp/transactions`** : Récupère les transactions
  - Paramètres optionnels : `?bien_id=int` ou `?user_id=int`
  - Tri : Par date décroissante
  - Réponse : `{'transactions': [...], 'total': int}`

- **`POST /api/lmnp/transactions`** : Crée une nouvelle transaction
  - Body : `{'bien_id': int, 'libelle': string, 'montant': number, ...}`
  - Date par défaut : Aujourd'hui si non spécifiée
  - Source automatique : 'manuel'

#### **Calculs Fiscaux**

- **`POST /api/lmnp/calcul-fiscal`** : Effectue un calcul fiscal complet
  - Body : `{'user_id': int, 'annee'?: int}`
  - Logique :
    1. Récupère tous les biens de l'utilisateur
    2. Agrège les transactions par année
    3. Calcule les totaux recettes/charges
    4. Compare micro-BIC vs régime réel
    5. Recommande le régime optimal
  - Réponse : Analyse détaillée avec recommandations

### 6.2 Blueprint Agents IA (`/api/agents`)

Ce blueprint gère les fonctionnalités d'intelligence artificielle.

#### **Gestion des Agents**

- **`GET /api/agents/agents`** : Liste les agents IA disponibles
  - Réponse : `{'agents': [...], 'total': int, 'orchestrateur_disponible': bool}`
  - Agents disponibles :
    - **Agent Accueil** : Onboarding et guide utilisateur
    - **Agent Fiscal** : Expert réglementation et optimisation
    - **Agent Comptable** : Catégorisation et analyse financière

#### **Chat Conversationnel**

- **`POST /api/agents/chat`** : Chat avec sélection automatique d'agent
  - Body : `{'message': string, 'contexte'?: object}`
  - Utilise l'orchestrateur pour router vers l'agent approprié
  - Réponse : `{'response': string, 'agent_utilise': string, 'confiance': float}`

#### **Services IA Spécialisés**

- **`POST /api/agents/analyze-transaction`** : Analyse automatique de transaction
  - Body : `{'libelle': string, 'montant': number}`
  - Logique :
    - Catégorisation par mots-clés
    - Détermination type (recette/charge)
    - Calcul niveau de confiance
  - Réponse : Catégorie, type, suggestions comptables

- **`POST /api/agents/optimize-fiscal`** : Optimisation fiscale
  - Body : `{'recettes': number, 'charges': number, 'type_location'?: string}`
  - Compare micro-BIC vs régime réel
  - Calcule l'économie potentielle
  - Fournit des conseils personnalisés

### 6.3 Routes Système (dans `main.py`)

#### **Documentation et Monitoring**

- **`GET /api`** : Page d'accueil de l'API avec présentation
- **`GET /api/health`** : Vérification de l'état de santé
  - Teste la connexion base de données
  - Vérifie la disponibilité des clés API
  - Réponse : Statut global et détail des composants

- **`GET /api/docs`** : Documentation interactive de l'API
  - Liste tous les endpoints avec exemples
  - Formats de requête/réponse
  - Codes d'erreur

#### **Gestion des Erreurs**

- **404** : Endpoint non trouvé avec suggestions
- **500** : Erreur interne avec logging automatique

#### **Sécurité et Middleware**

- **CORS** : Configuration cross-origin pour le frontend
- **Headers de sécurité** : X-Content-Type-Options, X-Frame-Options, X-XSS-Protection
- **Logging des requêtes** : Journalisation automatique de toutes les requêtes API

---

## 7. Services Métier

### 7.1 Expertise Fiscale (`expertise_fiscale_lmnp.py`)

Service spécialisé dans les calculs fiscaux LMNP :
- Gestion des seuils réglementaires 2024-2025
- Calculs micro-BIC avec abattements
- Calculs régime réel avec amortissements
- Optimisation automatique des régimes

### 7.2 Agents IA (`agents_ia_simple_lmnp.py`)

Orchestrateur d'agents intelligents :
- **Agent Accueil** : Onboarding personnalisé
- **Agent Fiscal** : Expertise réglementaire
- **Agent Comptable** : Catégorisation automatique
- Routage intelligent des demandes utilisateur

---

## 8. Configuration et Déploiement

### 8.1 Variables d'Environnement

Le fichier `.env` contient :
```
SECRET_KEY=lmnp-saas-production-secret-key-2025
OPENAI_API_KEY=your_openai_api_key_here
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
LOG_LEVEL=INFO
FLASK_ENV=development
```

### 8.2 Dépendances (`requirements.txt`)

Principales dépendances :
- **Flask** : Framework web
- **Flask-SQLAlchemy** : ORM base de données
- **Flask-CORS** : Gestion cross-origin
- **OpenAI** : API d'intelligence artificielle
- **Decimal** : Calculs financiers précis

### 8.3 Structure de Déploiement

```
backend/
├── src/
│   ├── main.py              # Point d'entrée
│   ├── database_config.py   # Configuration DB
│   ├── models/              # Modèles de données
│   ├── routes/              # Endpoints API
│   ├── services/            # Logique métier
│   └── static/              # Fichiers statiques frontend
└── database/
    └── app.db              # Base de données SQLite
```

Le backend peut servir les fichiers statiques du frontend en production, permettant un déploiement unifié sur un seul serveur.

