# Architecture Frontend - LMNP SAAS

Ce document détaille l'architecture du frontend de l'application LMNP SAAS, construite avec React et Vite.



## 1. Vue d'ensemble de l'architecture

Le frontend de l'application LMNP SAAS est construit avec **React 19** et **Vite** comme bundler. Il suit une architecture moderne basée sur des composants fonctionnels avec hooks, et utilise **React Router** pour la navigation.

### Technologies principales :
- **React 19** : Framework JavaScript pour l'interface utilisateur
- **Vite** : Bundler et serveur de développement ultra-rapide
- **React Router DOM** : Gestion du routage côté client
- **Tailwind CSS** : Framework CSS utilitaire pour le styling
- **Radix UI** : Bibliothèque de composants accessibles
- **Lucide React** : Bibliothèque d'icônes
- **Recharts** : Bibliothèque de graphiques pour React

---

## 2. Structure des Fichiers et Dossiers

```
frontend/
├── public/                    # Fichiers statiques publics
├── src/
│   ├── main.jsx              # Point d'entrée de l'application
│   ├── App.jsx               # Composant principal avec routage
│   ├── App.css               # Styles spécifiques à l'application
│   ├── index.css             # Styles globaux et Tailwind
│   ├── components/           # Composants React
│   │   ├── LoginPage.jsx     # Page de connexion/inscription
│   │   └── ui/               # Composants UI réutilisables (Radix UI)
│   │       ├── button.jsx
│   │       ├── card.jsx
│   │       ├── input.jsx
│   │       ├── select.jsx
│   │       └── ... (40+ composants)
│   ├── lib/                  # Utilitaires et helpers
│   │   └── utils.js          # Fonctions utilitaires (clsx, tailwind-merge)
│   ├── hooks/                # Hooks React personnalisés
│   └── assets/               # Images, fonts, etc.
├── package.json              # Dépendances et scripts
├── vite.config.js            # Configuration Vite
├── tailwind.config.js        # Configuration Tailwind CSS
└── components.json           # Configuration des composants UI
```

---

## 3. Architecture des Composants

### 3.1 Composant Principal (`App.jsx`)

Le fichier `App.jsx` est le cœur de l'application frontend. Il contient :

#### **Service API (`LMNPApiService`)**
Une classe statique qui centralise toutes les communications avec le backend :

```javascript
class LMNPApiService {
  static async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`
    const response = await fetch(url, {
      headers: { 'Content-Type': 'application/json', ...options.headers },
      ...options,
    })
    if (!response.ok) throw new Error(error.error || 'Erreur API')
    return response.json()
  }

  // Méthodes pour chaque endpoint :
  static async createUser(userData) { /* ... */ }
  static async getBiens(userId) { /* ... */ }
  static async createBien(userId, bienData) { /* ... */ }
  static async getCalculsFiscaux(userId, annee) { /* ... */ }
  // ... autres méthodes
}
```

#### **Composants Fonctionnels Principaux**

1. **`Dashboard({ userId })`** : Tableau de bord avec statistiques
2. **`GestionBiens({ userId })`** : Gestion des biens immobiliers
3. **`CalculsFiscaux({ userId })`** : Calculs et optimisations fiscales
4. **`MainApp()`** : Application principale avec navigation
5. **`OnboardingFlow({ onComplete })`** : Processus d'accueil

### 3.2 Gestion de l'État

L'application utilise les **hooks React** pour la gestion d'état :

- **`useState`** : État local des composants
- **`useEffect`** : Effets de bord et chargement de données
- **`localStorage`** : Persistance de la session utilisateur

```javascript
const [currentUser, setCurrentUser] = useState(null)
const [isAuthenticated, setIsAuthenticated] = useState(false)

// Persistance de la session
useEffect(() => {
  const savedUser = localStorage.getItem('lmnp_user')
  if (savedUser) {
    const user = JSON.parse(savedUser)
    setCurrentUser(user)
    setIsAuthenticated(true)
  }
}, [])
```

### 3.3 Routage et Navigation

L'application utilise **React Router DOM** pour la navigation :

```javascript
<Router>
  <Routes>
    <Route path="/" element={<Dashboard userId={currentUser.id} />} />
    <Route path="/biens" element={<GestionBiens userId={currentUser.id} />} />
    <Route path="/calculs" element={<CalculsFiscaux userId={currentUser.id} />} />
    <Route path="*" element={<div>Page en construction</div>} />
  </Routes>
</Router>
```

**Pages disponibles :**
- `/` : Dashboard principal
- `/biens` : Gestion des biens immobiliers
- `/transactions` : Gestion des transactions (en construction)
- `/calculs` : Calculs fiscaux
- `/declarations` : Déclarations fiscales (en construction)

---

## 4. Composant d'Authentification (`LoginPage.jsx`)

### 4.1 Fonctionnalités

Le composant `LoginPage` gère :
- **Connexion** avec email/mot de passe
- **Inscription** de nouveaux utilisateurs
- **Mode démo** pour tester l'application
- **Validation** des formulaires
- **Gestion des erreurs** avec feedback utilisateur

### 4.2 État et Gestion des Formulaires

```javascript
const [formData, setFormData] = useState({
  email: '',
  password: ''
})
const [showPassword, setShowPassword] = useState(false)
const [loading, setLoading] = useState(false)
const [error, setError] = useState('')
const [isSignUp, setIsSignUp] = useState(false)
```

### 4.3 Simulation d'Authentification

Pour la démo, l'authentification est simulée :

```javascript
const handleSubmit = async (e) => {
  e.preventDefault()
  if (!validateForm()) return
  
  setLoading(true)
  // Simulation d'appel API
  await new Promise(resolve => setTimeout(resolve, 1500))
  
  const user = {
    id: 1,
    email: formData.email,
    nom: 'Martin',
    prenom: 'Jean'
  }
  onLogin(user)
}
```

---

## 5. Système de Composants UI

### 5.1 Bibliothèque Radix UI

L'application utilise **Radix UI** comme base pour les composants :
- **Accessibilité** : Composants conformes aux standards ARIA
- **Personnalisation** : Styling avec Tailwind CSS
- **Consistance** : Design system unifié

### 5.2 Composants Disponibles

**Composants de base :**
- `Button` : Boutons avec variantes (primary, outline, ghost)
- `Input` : Champs de saisie avec validation
- `Select` : Listes déroulantes
- `Textarea` : Zones de texte multilignes
- `Label` : Étiquettes de formulaires

**Composants de layout :**
- `Card` : Conteneurs avec header/content/footer
- `Tabs` : Onglets pour organiser le contenu
- `Dialog` : Modales et popups
- `Sheet` : Panneaux latéraux

**Composants de feedback :**
- `Alert` : Messages d'alerte et notifications
- `Badge` : Étiquettes et statuts
- `Progress` : Barres de progression
- `Skeleton` : Placeholders de chargement

### 5.3 Exemple d'Utilisation

```javascript
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'

function MonComposant() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Titre de la carte</CardTitle>
      </CardHeader>
      <CardContent>
        <Input placeholder="Saisir du texte" />
        <Button className="mt-4">Valider</Button>
      </CardContent>
    </Card>
  )
}
```

---

## 6. Styling et Design System

### 6.1 Tailwind CSS

L'application utilise **Tailwind CSS** pour le styling :
- **Utility-first** : Classes utilitaires pour un développement rapide
- **Responsive** : Design adaptatif mobile-first
- **Customisation** : Palette de couleurs et thème personnalisés

### 6.2 Configuration Tailwind

```javascript
// tailwind.config.js
module.exports = {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          900: '#1e3a8a'
        }
      }
    }
  },
  plugins: []
}
```

### 6.3 Classes Utilitaires Personnalisées

```css
/* App.css */
.gradient-bg {
  @apply bg-gradient-to-br from-blue-50 via-white to-purple-50;
}

.card-shadow {
  @apply shadow-lg border-0;
}

.loading-spinner {
  @apply animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600;
}
```

---

## 7. Gestion des Données et API

### 7.1 Communication avec le Backend

Toutes les communications avec l'API backend passent par la classe `LMNPApiService` :

```javascript
const API_BASE_URL = '/api/lmnp'

// Exemple d'appel API
const loadBiens = async () => {
  try {
    const data = await LMNPApiService.getBiens(userId)
    setBiens(data.biens || [])
  } catch (error) {
    console.error('Erreur chargement biens:', error)
    setBiens([])
  }
}
```

### 7.2 Gestion des Erreurs

```javascript
static async request(endpoint, options = {}) {
  const response = await fetch(url, options)
  
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.error || 'Erreur API')
  }
  
  return response.json()
}
```

### 7.3 États de Chargement

```javascript
const [loading, setLoading] = useState(true)

const loadData = async () => {
  setLoading(true)
  try {
    const data = await LMNPApiService.getData()
    setData(data)
  } finally {
    setLoading(false)
  }
}

// Affichage conditionnel
if (loading) {
  return <div className="loading-spinner"></div>
}
```

---

## 8. Fonctionnalités Principales

### 8.1 Dashboard

**Composant :** `Dashboard({ userId })`

**Fonctionnalités :**
- Statistiques en temps réel (nombre de biens, recettes, charges)
- Graphiques de performance
- Dernières transactions
- Assistant IA intégré

**Structure :**
```javascript
function Dashboard({ userId }) {
  const [dashboardData, setDashboardData] = useState(null)
  
  useEffect(() => {
    loadDashboard()
  }, [userId])
  
  return (
    <div className="space-y-6">
      {/* En-tête avec agent IA */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600">
        {/* Contenu */}
      </div>
      
      {/* Statistiques principales */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {/* Cartes de statistiques */}
      </div>
    </div>
  )
}
```

### 8.2 Gestion des Biens

**Composant :** `GestionBiens({ userId })`

**Fonctionnalités :**
- Liste des biens immobiliers
- Formulaire de création/édition
- Validation des données
- Affichage en grille responsive

**Formulaire de création :**
```javascript
const [formData, setFormData] = useState({
  nom: '',
  adresse: '',
  code_postal: '',
  ville: '',
  type_location: '',
  surface: '',
  nb_pieces: '',
  date_acquisition: '',
  prix_acquisition: ''
})

const handleSubmit = async (e) => {
  e.preventDefault()
  try {
    await LMNPApiService.createBien(userId, formData)
    setShowForm(false)
    await loadBiens()
  } catch (error) {
    alert('Erreur lors de la création du bien: ' + error.message)
  }
}
```

### 8.3 Calculs Fiscaux

**Composant :** `CalculsFiscaux({ userId })`

**Fonctionnalités :**
- Sélection de l'année fiscale
- Comparaison micro-BIC vs régime réel
- Détail des amortissements
- Recommandations d'optimisation

---

## 9. Configuration et Build

### 9.1 Scripts NPM

```json
{
  "scripts": {
    "dev": "vite",              // Serveur de développement
    "build": "vite build",      // Build de production
    "lint": "eslint .",         // Vérification du code
    "preview": "vite preview"   // Aperçu du build
  }
}
```

### 9.2 Configuration Vite

```javascript
// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  }
})
```

### 9.3 Déploiement

**Développement :**
```bash
npm run dev  # Serveur sur http://localhost:5173
```

**Production :**
```bash
npm run build  # Génère le dossier dist/
npm run preview  # Aperçu du build de production
```

---

## 10. Bonnes Pratiques Implémentées

### 10.1 Structure des Composants

- **Composants fonctionnels** avec hooks
- **Séparation des responsabilités** (UI, logique, API)
- **Props typing** implicite avec JSX
- **Gestion d'état locale** avec useState

### 10.2 Performance

- **Lazy loading** des composants (à implémenter)
- **Memoization** avec useMemo/useCallback (à optimiser)
- **Bundle splitting** automatique avec Vite
- **Tree shaking** pour réduire la taille du bundle

### 10.3 Accessibilité

- **Composants Radix UI** conformes ARIA
- **Navigation au clavier** supportée
- **Contrastes de couleurs** respectés
- **Labels sémantiques** sur tous les formulaires

### 10.4 Responsive Design

- **Mobile-first** avec Tailwind CSS
- **Breakpoints** : sm (640px), md (768px), lg (1024px)
- **Grilles flexibles** avec CSS Grid et Flexbox
- **Images adaptatives** (à implémenter)

---

## 11. Améliorations Futures

### 11.1 Fonctionnalités à Développer

- **Pages Transactions et Déclarations** (actuellement en construction)
- **Upload de documents** avec OCR
- **Graphiques avancés** avec Recharts
- **Mode sombre** avec next-themes
- **Notifications** avec Sonner

### 11.2 Optimisations Techniques

- **State management** avec Zustand ou Redux Toolkit
- **Cache des requêtes** avec React Query
- **Tests unitaires** avec Vitest et Testing Library
- **Storybook** pour la documentation des composants

### 11.3 UX/UI

- **Animations** avec Framer Motion
- **Skeleton loaders** pendant les chargements
- **Feedback utilisateur** amélioré
- **Onboarding interactif** pour les nouveaux utilisateurs

L'architecture frontend est conçue pour être **scalable**, **maintenable** et **performante**, avec une base solide pour les développements futurs.

