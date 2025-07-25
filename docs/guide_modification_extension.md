# Guide de Modification et d'Extension - LMNP SAAS

Ce guide vous explique comment modifier et étendre l'application LMNP SAAS de manière autonome.

---

## 1. Préparation de l'Environnement de Développement

### 1.1 Prérequis

- **Python 3.11+** avec pip
- **Node.js 20+** avec npm
- **Git** pour le versioning
- **VS Code** (recommandé) avec extensions Python et React

### 1.2 Installation

```bash
# Cloner le projet
git clone https://github.com/skanderbour/lmnp-saas.git
cd lmnp-saas

# Backend
cd backend
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env
# Éditer .env avec vos clés API

# Frontend
cd ../frontend
npm install

# Lancer l'application
# Terminal 1 - Backend
cd backend/src && python main.py

# Terminal 2 - Frontend
cd frontend && npm run dev
```

### 1.3 Structure de développement recommandée

```
lmnp-saas/
├── docs/                    # Documentation (ce guide)
├── backend/
│   ├── src/
│   │   ├── main.py         # Point d'entrée - MODIFIER ICI pour nouvelles routes
│   │   ├── models/         # AJOUTER ICI nouveaux modèles de données
│   │   ├── routes/         # AJOUTER ICI nouvelles routes API
│   │   └── services/       # AJOUTER ICI nouvelle logique métier
│   └── tests/              # CRÉER ICI vos tests
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # MODIFIER ICI pour nouvelles pages
│   │   ├── components/     # AJOUTER ICI nouveaux composants
│   │   └── services/       # AJOUTER ICI services API
│   └── tests/              # CRÉER ICI vos tests frontend
└── scripts/                # Scripts utilitaires
```

---

## 2. Modification du Backend

### 2.1 Ajouter un Nouveau Modèle de Données

#### Étape 1 : Créer le modèle

Créez un fichier dans `backend/src/models/` :

```python
# backend/src/models/nouveau_modele.py
from src.database_config import db
from datetime import datetime

class NouveauModele(db.Model):
    __tablename__ = 'nouveau_modele'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    actif = db.Column(db.Boolean, default=True)
    
    # Relations (exemple)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'description': self.description,
            'date_creation': self.date_creation.isoformat() if self.date_creation else None,
            'actif': self.actif,
            'user_id': self.user_id
        }
    
    def __repr__(self):
        return f'<NouveauModele {self.nom}>'
```

#### Étape 2 : Importer dans database_config.py

```python
# backend/src/database_config.py
def init_database(app):
    # ... code existant ...
    
    with app.app_context():
        # Import des modèles existants
        from src.models.user import User
        from src.models.lmnp_models import (
            User as LMNPUser, BienImmobilier, Transaction, 
            DeclarationFiscale, Document
        )
        # AJOUTER ICI votre nouveau modèle
        from src.models.nouveau_modele import NouveauModele
        
        # Création des tables
        db.create_all()
```

#### Étape 3 : Redémarrer l'application

```bash
# Arrêter le serveur (Ctrl+C)
# Relancer
cd backend/src && python main.py
```

### 2.2 Ajouter de Nouvelles Routes API

#### Étape 1 : Créer le fichier de routes

```python
# backend/src/routes/nouveau_routes.py
from flask import Blueprint, request, jsonify, current_app
from src.database_config import db
from src.models.nouveau_modele import NouveauModele

# Créer le blueprint
nouveau_bp = Blueprint('nouveau', __name__)

@nouveau_bp.route('/items', methods=['GET'])
def get_items():
    """Récupération de tous les items"""
    try:
        items = NouveauModele.query.filter_by(actif=True).all()
        return jsonify({
            'items': [item.to_dict() for item in items],
            'total': len(items)
        })
    except Exception as e:
        current_app.logger.error(f"Erreur get_items: {e}")
        return jsonify({'error': str(e)}), 500

@nouveau_bp.route('/items', methods=['POST'])
def create_item():
    """Création d'un nouvel item"""
    try:
        data = request.get_json()
        
        if not data or 'nom' not in data:
            return jsonify({'error': 'Nom requis'}), 400
        
        item = NouveauModele(
            nom=data['nom'],
            description=data.get('description'),
            user_id=data.get('user_id')
        )
        
        db.session.add(item)
        db.session.commit()
        
        return jsonify({
            'message': 'Item créé avec succès',
            'item': item.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erreur create_item: {e}")
        return jsonify({'error': str(e)}), 500

@nouveau_bp.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """Mise à jour d'un item"""
    try:
        item = NouveauModele.query.get_or_404(item_id)
        data = request.get_json()
        
        if 'nom' in data:
            item.nom = data['nom']
        if 'description' in data:
            item.description = data['description']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Item mis à jour avec succès',
            'item': item.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erreur update_item: {e}")
        return jsonify({'error': str(e)}), 500

@nouveau_bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Suppression d'un item (soft delete)"""
    try:
        item = NouveauModele.query.get_or_404(item_id)
        item.actif = False
        db.session.commit()
        
        return jsonify({'message': 'Item supprimé avec succès'})
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erreur delete_item: {e}")
        return jsonify({'error': str(e)}), 500
```

#### Étape 2 : Enregistrer le blueprint

```python
# backend/src/main.py
def create_app():
    # ... code existant ...
    
    # Import des routes existantes
    from src.routes.unified_routes import lmnp_bp, agents_bp
    # AJOUTER ICI votre nouveau blueprint
    from src.routes.nouveau_routes import nouveau_bp
    
    # Enregistrement des blueprints
    app.register_blueprint(lmnp_bp, url_prefix='/api/lmnp')
    app.register_blueprint(agents_bp, url_prefix='/api/agents')
    # AJOUTER ICI l'enregistrement
    app.register_blueprint(nouveau_bp, url_prefix='/api/nouveau')
    
    # ... reste du code ...
```

### 2.3 Ajouter un Service Métier

```python
# backend/src/services/nouveau_service.py
from typing import Dict, List, Optional
from src.models.nouveau_modele import NouveauModele
from src.database_config import db

class NouveauService:
    """Service métier pour la gestion des nouveaux items"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def calculer_statistiques(self, user_id: int) -> Dict:
        """Calcule les statistiques pour un utilisateur"""
        try:
            items = NouveauModele.query.filter_by(
                user_id=user_id, 
                actif=True
            ).all()
            
            return {
                'total_items': len(items),
                'items_recents': len([i for i in items if self._is_recent(i.date_creation)]),
                'moyenne_par_mois': self._calculer_moyenne_mensuelle(items)
            }
        except Exception as e:
            self.logger.error(f"Erreur calcul statistiques: {e}")
            return {'error': str(e)}
    
    def _is_recent(self, date_creation) -> bool:
        """Vérifie si un item est récent (moins de 30 jours)"""
        from datetime import datetime, timedelta
        return (datetime.now() - date_creation) < timedelta(days=30)
    
    def _calculer_moyenne_mensuelle(self, items: List) -> float:
        """Calcule la moyenne mensuelle d'items"""
        if not items:
            return 0.0
        
        # Logique de calcul personnalisée
        return len(items) / 12  # Exemple simple
```

### 2.4 Tester les Modifications Backend

```python
# backend/tests/test_nouveau_modele.py
import unittest
from src.main import create_app
from src.database_config import db, init_database
from src.models.nouveau_modele import NouveauModele

class TestNouveauModele(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with self.app.app_context():
            init_database(self.app)
            db.create_all()
        
        self.client = self.app.test_client()
    
    def test_create_item(self):
        """Test création d'un item"""
        with self.app.app_context():
            item = NouveauModele(
                nom='Test Item',
                description='Description test',
                user_id=1
            )
            db.session.add(item)
            db.session.commit()
            
            self.assertEqual(item.nom, 'Test Item')
            self.assertTrue(item.actif)
    
    def test_api_create_item(self):
        """Test API de création"""
        response = self.client.post('/api/nouveau/items', 
            json={
                'nom': 'Test API',
                'description': 'Test via API',
                'user_id': 1
            }
        )
        
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['item']['nom'], 'Test API')

if __name__ == '__main__':
    unittest.main()
```

---

## 3. Modification du Frontend

### 3.1 Ajouter un Nouveau Composant

#### Étape 1 : Créer le composant

```javascript
// frontend/src/components/NouveauComposant.jsx
import React, { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Plus, Edit3, Trash2 } from 'lucide-react'

// Service API pour le nouveau composant
class NouveauApiService {
  static async getItems() {
    const response = await fetch('/api/nouveau/items')
    if (!response.ok) throw new Error('Erreur chargement items')
    return response.json()
  }
  
  static async createItem(itemData) {
    const response = await fetch('/api/nouveau/items', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(itemData)
    })
    if (!response.ok) throw new Error('Erreur création item')
    return response.json()
  }
  
  static async updateItem(itemId, itemData) {
    const response = await fetch(`/api/nouveau/items/${itemId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(itemData)
    })
    if (!response.ok) throw new Error('Erreur mise à jour item')
    return response.json()
  }
  
  static async deleteItem(itemId) {
    const response = await fetch(`/api/nouveau/items/${itemId}`, {
      method: 'DELETE'
    })
    if (!response.ok) throw new Error('Erreur suppression item')
    return response.json()
  }
}

function NouveauComposant({ userId }) {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingItem, setEditingItem] = useState(null)
  const [formData, setFormData] = useState({
    nom: '',
    description: ''
  })

  // Chargement des données
  useEffect(() => {
    loadItems()
  }, [])

  const loadItems = async () => {
    try {
      setLoading(true)
      const data = await NouveauApiService.getItems()
      setItems(data.items || [])
    } catch (error) {
      console.error('Erreur chargement items:', error)
      setItems([])
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    try {
      const itemData = { ...formData, user_id: userId }
      
      if (editingItem) {
        await NouveauApiService.updateItem(editingItem.id, itemData)
      } else {
        await NouveauApiService.createItem(itemData)
      }
      
      // Réinitialiser le formulaire
      setFormData({ nom: '', description: '' })
      setShowForm(false)
      setEditingItem(null)
      
      // Recharger les données
      await loadItems()
      
    } catch (error) {
      console.error('Erreur sauvegarde:', error)
      alert('Erreur lors de la sauvegarde: ' + error.message)
    }
  }

  const handleEdit = (item) => {
    setEditingItem(item)
    setFormData({
      nom: item.nom,
      description: item.description || ''
    })
    setShowForm(true)
  }

  const handleDelete = async (itemId) => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cet item ?')) return
    
    try {
      await NouveauApiService.deleteItem(itemId)
      await loadItems()
    } catch (error) {
      console.error('Erreur suppression:', error)
      alert('Erreur lors de la suppression: ' + error.message)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">Mes Items</h2>
        <Button onClick={() => setShowForm(true)}>
          <Plus className="h-4 w-4 mr-2" />
          Ajouter un item
        </Button>
      </div>

      {/* Formulaire */}
      {showForm && (
        <Card>
          <CardHeader>
            <CardTitle>
              {editingItem ? 'Modifier l\'item' : 'Nouvel Item'}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <Label htmlFor="nom">Nom *</Label>
                <Input
                  id="nom"
                  value={formData.nom}
                  onChange={(e) => setFormData({...formData, nom: e.target.value})}
                  required
                />
              </div>
              <div>
                <Label htmlFor="description">Description</Label>
                <Input
                  id="description"
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                />
              </div>
              <div className="flex justify-end space-x-2">
                <Button 
                  type="button" 
                  variant="outline" 
                  onClick={() => {
                    setShowForm(false)
                    setEditingItem(null)
                    setFormData({ nom: '', description: '' })
                  }}
                >
                  Annuler
                </Button>
                <Button type="submit">
                  {editingItem ? 'Mettre à jour' : 'Créer'}
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

      {/* Liste des items */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {items.map((item) => (
          <Card key={item.id}>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span>{item.nom}</span>
                <div className="flex space-x-1">
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => handleEdit(item)}
                  >
                    <Edit3 className="h-4 w-4" />
                  </Button>
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => handleDelete(item.id)}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600">{item.description}</p>
              <p className="text-xs text-gray-400 mt-2">
                Créé le {new Date(item.date_creation).toLocaleDateString('fr-FR')}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      {items.length === 0 && (
        <Card>
          <CardContent className="text-center py-8">
            <p className="text-gray-500">Aucun item enregistré</p>
            <Button className="mt-4" onClick={() => setShowForm(true)}>
              Créer votre premier item
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

export default NouveauComposant
```

#### Étape 2 : Ajouter la route dans App.jsx

```javascript
// frontend/src/App.jsx
import NouveauComposant from './components/NouveauComposant.jsx'

function MainApp() {
  // ... code existant ...

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        {/* Navigation */}
        <nav className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                {/* ... navigation existante ... */}
                <div className="hidden md:ml-6 md:flex md:space-x-8">
                  {/* ... liens existants ... */}
                  
                  {/* AJOUTER ICI votre nouveau lien */}
                  <Link to="/nouveau" className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-blue-600">
                    <Plus className="h-4 w-4 mr-1" />
                    Nouveau
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </nav>

        {/* Contenu principal */}
        <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="px-4 py-6 sm:px-0">
            <Routes>
              {/* ... routes existantes ... */}
              
              {/* AJOUTER ICI votre nouvelle route */}
              <Route path="/nouveau" element={<NouveauComposant userId={currentUser.id} />} />
              
              <Route path="*" element={<div className="text-center">Page en construction</div>} />
            </Routes>
          </div>
        </main>
      </div>
    </Router>
  )
}
```

### 3.2 Modifier un Composant Existant

#### Exemple : Ajouter un champ au formulaire de création de bien

```javascript
// frontend/src/App.jsx - Dans le composant GestionBiens
function GestionBiens({ userId }) {
  const [formData, setFormData] = useState({
    nom: '',
    adresse: '',
    code_postal: '',
    ville: '',
    type_location: '',
    surface: '',
    nb_pieces: '',
    date_acquisition: '',
    prix_acquisition: '',
    // AJOUTER ICI vos nouveaux champs
    nouveau_champ: '',
    autre_champ: ''
  })

  // Dans le JSX du formulaire, ajouter :
  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* ... champs existants ... */}
      
      {/* AJOUTER ICI vos nouveaux champs */}
      <div>
        <Label htmlFor="nouveau_champ">Nouveau Champ</Label>
        <Input
          id="nouveau_champ"
          value={formData.nouveau_champ}
          onChange={(e) => setFormData({...formData, nouveau_champ: e.target.value})}
        />
      </div>
      
      <div>
        <Label htmlFor="autre_champ">Autre Champ</Label>
        <Select 
          value={formData.autre_champ} 
          onValueChange={(value) => setFormData({...formData, autre_champ: value})}
        >
          <SelectTrigger>
            <SelectValue placeholder="Sélectionner une option" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="option1">Option 1</SelectItem>
            <SelectItem value="option2">Option 2</SelectItem>
          </SelectContent>
        </Select>
      </div>
      
      {/* ... reste du formulaire ... */}
    </form>
  )
}
```

### 3.3 Ajouter un Nouveau Composant UI

```javascript
// frontend/src/components/ui/nouveau-composant.jsx
import React from 'react'
import { cn } from '@/lib/utils.js'

const NouveauComposantUI = React.forwardRef(({ className, variant = "default", size = "default", ...props }, ref) => {
  return (
    <div
      className={cn(
        // Classes de base
        "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
        "disabled:pointer-events-none disabled:opacity-50",
        
        // Variantes
        {
          "bg-primary text-primary-foreground hover:bg-primary/90": variant === "default",
          "bg-secondary text-secondary-foreground hover:bg-secondary/80": variant === "secondary",
          "border border-input bg-background hover:bg-accent": variant === "outline",
        },
        
        // Tailles
        {
          "h-10 px-4 py-2": size === "default",
          "h-9 rounded-md px-3": size === "sm",
          "h-11 rounded-md px-8": size === "lg",
        },
        
        className
      )}
      ref={ref}
      {...props}
    />
  )
})

NouveauComposantUI.displayName = "NouveauComposantUI"

export { NouveauComposantUI }
```

---

## 4. Ajouter de Nouvelles Fonctionnalités

### 4.1 Ajouter un Nouvel Agent IA

#### Étape 1 : Créer la classe d'agent

```python
# backend/src/services/agents_ia_simple_lmnp.py

class AgentNouveauSimple(BaseAgentSimple):
    """Nouvel agent spécialisé"""
    
    def __init__(self):
        super().__init__(
            name="Agent Nouveau",
            description="Description de votre nouvel agent",
            temperature=0.5
        )
        # Initialisation spécifique
        self.knowledge_base = self._create_knowledge_base()
    
    def _get_system_prompt(self) -> str:
        return """Tu es l'Agent Nouveau, spécialisé dans [VOTRE DOMAINE].

Ton rôle est de :
1. [Responsabilité 1]
2. [Responsabilité 2]
3. [Responsabilité 3]

Tu dois être :
- [Caractéristique 1]
- [Caractéristique 2]
- [Caractéristique 3]

Utilise les données des outils pour [OBJECTIF]."""
    
    def _process_tools(self, message: str, context: Optional[Dict] = None) -> Dict:
        """Traite les outils spécifiques au nouvel agent"""
        result = {}
        message_lower = message.lower()
        
        # Logique spécifique à votre agent
        if 'mot_cle' in message_lower:
            result['fonctionnalite'] = self._ma_fonctionnalite(context)
        
        return result
    
    def _ma_fonctionnalite(self, context: Optional[Dict] = None) -> Dict:
        """Implémente une fonctionnalité spécifique"""
        # Votre logique ici
        return {'resultat': 'Ma logique métier'}
    
    def _create_knowledge_base(self) -> Dict:
        """Crée la base de connaissances spécialisée"""
        return {
            'concepts': {
                'concept1': 'Définition du concept 1',
                'concept2': 'Définition du concept 2'
            },
            'regles': [
                'Règle métier 1',
                'Règle métier 2'
            ]
        }
```

#### Étape 2 : Ajouter à l'orchestrateur

```python
# Dans la classe OrchestrateurAgentsSimple
def __init__(self):
    self.agents = {
        'accueil': AgentAccueilSimple(),
        'fiscal': AgentFiscalSimple(),
        'comptable': AgentComptableSimple(),
        # AJOUTER ICI votre nouvel agent
        'nouveau': AgentNouveauSimple()
    }
    self.conversation_history = []

def _select_best_agent(self, message: str, context: Dict = None) -> str:
    # Mots-clés pour chaque agent
    keywords = {
        'accueil': ['bonjour', 'aide', 'commencer'],
        'fiscal': ['impôt', 'fiscal', 'régime'],
        'comptable': ['transaction', 'catégorie', 'charge'],
        # AJOUTER ICI les mots-clés de votre agent
        'nouveau': ['nouveau_mot_cle', 'autre_mot_cle']
    }
    
    # ... reste de la logique
```

#### Étape 3 : Mettre à jour les routes

```python
# backend/src/routes/unified_routes.py
@agents_bp.route('/agents', methods=['GET'])
def get_agents():
    """Liste des agents IA disponibles"""
    try:
        agents = [
            # ... agents existants ...
            {
                'id': 'agent_nouveau',
                'nom': 'Agent Nouveau',
                'description': 'Description de votre nouvel agent',
                'specialites': ['specialite1', 'specialite2'],
                'disponible': agents_available
            }
        ]
        
        return jsonify({
            'agents': agents,
            'total': len(agents),
            'orchestrateur_disponible': agents_available
        })
    except Exception as e:
        current_app.logger.error(f"Erreur get_agents: {e}")
        return jsonify({'error': str(e)}), 500
```

### 4.2 Ajouter une Nouvelle Page Frontend

#### Étape 1 : Créer le composant de page

```javascript
// frontend/src/components/NouvellePage.jsx
import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'

function NouvellePage({ userId }) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadData()
  }, [userId])

  const loadData = async () => {
    try {
      setLoading(true)
      // Appel à votre nouvelle API
      const response = await fetch(`/api/nouveau/data?user_id=${userId}`)
      const result = await response.json()
      setData(result)
    } catch (error) {
      console.error('Erreur chargement données:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="text-center">Chargement...</div>
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Ma Nouvelle Page</h1>
      
      <Card>
        <CardHeader>
          <CardTitle>Contenu Principal</CardTitle>
        </CardHeader>
        <CardContent>
          <p>Contenu de votre nouvelle page</p>
          {data && (
            <pre>{JSON.stringify(data, null, 2)}</pre>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

export default NouvellePage
```

#### Étape 2 : Ajouter la route

```javascript
// frontend/src/App.jsx
import NouvellePage from './components/NouvellePage.jsx'

// Dans les Routes
<Routes>
  {/* ... routes existantes ... */}
  <Route path="/nouvelle-page" element={<NouvellePage userId={currentUser.id} />} />
</Routes>

// Dans la navigation
<Link to="/nouvelle-page" className="...">
  Nouvelle Page
</Link>
```

---

## 5. Débogage et Tests

### 5.1 Débogage Backend

#### Logs détaillés

```python
# Ajouter dans vos fonctions
import logging
logger = logging.getLogger(__name__)

def ma_fonction():
    logger.info("Début de ma_fonction")
    try:
        # Votre code
        logger.debug(f"Valeur variable: {variable}")
        result = operation()
        logger.info(f"Résultat: {result}")
        return result
    except Exception as e:
        logger.error(f"Erreur dans ma_fonction: {e}", exc_info=True)
        raise
```

#### Tests unitaires

```python
# backend/tests/test_ma_fonctionnalite.py
import unittest
from unittest.mock import patch, MagicMock
from src.services.mon_service import MonService

class TestMaFonctionnalite(unittest.TestCase):
    
    def setUp(self):
        self.service = MonService()
    
    def test_fonction_normale(self):
        """Test du cas normal"""
        result = self.service.ma_fonction('input_test')
        self.assertEqual(result, 'expected_output')
    
    def test_fonction_erreur(self):
        """Test de gestion d'erreur"""
        with self.assertRaises(ValueError):
            self.service.ma_fonction('input_invalide')
    
    @patch('src.services.mon_service.external_api')
    def test_avec_mock(self, mock_api):
        """Test avec mock d'API externe"""
        mock_api.return_value = {'status': 'success'}
        result = self.service.fonction_avec_api()
        self.assertTrue(result)
        mock_api.assert_called_once()

# Lancer les tests
# python -m pytest backend/tests/
```

### 5.2 Débogage Frontend

#### Console et logs

```javascript
// Logs détaillés
console.group('🔍 Chargement des données')
console.log('📡 Appel API:', endpoint)
console.log('📋 Paramètres:', params)

try {
  const response = await fetch(endpoint, params)
  console.log('✅ Réponse reçue:', response.status)
  
  const data = await response.json()
  console.log('📦 Données:', data)
  
  return data
} catch (error) {
  console.error('❌ Erreur:', error)
  throw error
} finally {
  console.groupEnd()
}
```

#### Tests avec React Testing Library

```javascript
// frontend/src/components/__tests__/MonComposant.test.jsx
import React from 'react'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import '@testing-library/jest-dom'
import MonComposant from '../MonComposant'

// Mock des APIs
jest.mock('../services/api', () => ({
  getData: jest.fn(() => Promise.resolve({ data: 'test' }))
}))

describe('MonComposant', () => {
  test('affiche le contenu correctement', () => {
    render(<MonComposant userId={1} />)
    
    expect(screen.getByText('Mon Titre')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /ajouter/i })).toBeInTheDocument()
  })
  
  test('gère le clic sur le bouton', async () => {
    render(<MonComposant userId={1} />)
    
    const button = screen.getByRole('button', { name: /ajouter/i })
    fireEvent.click(button)
    
    await waitFor(() => {
      expect(screen.getByText('Élément ajouté')).toBeInTheDocument()
    })
  })
})

// Lancer les tests
// npm test
```

---

## 6. Déploiement et Production

### 6.1 Préparation pour la Production

#### Variables d'environnement

```bash
# backend/.env.production
SECRET_KEY=your_production_secret_key_here
OPENAI_API_KEY=your_production_openai_key
FLASK_ENV=production
LOG_LEVEL=WARNING
CORS_ORIGINS=https://yourdomain.com

# frontend/.env.production
VITE_API_BASE_URL=https://api.yourdomain.com
VITE_APP_ENV=production
```

#### Build de production

```bash
# Frontend
cd frontend
npm run build
# Génère le dossier dist/

# Backend - copier les fichiers statiques
cp -r frontend/dist/* backend/src/static/
```

### 6.2 Optimisations

#### Backend

```python
# backend/src/main.py - Configuration production
def create_app():
    app = Flask(__name__)
    
    # Configuration sécurisée pour la production
    if os.environ.get('FLASK_ENV') == 'production':
        app.config['DEBUG'] = False
        app.config['TESTING'] = False
        
        # Headers de sécurité renforcés
        @app.after_request
        def security_headers(response):
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
            response.headers['Content-Security-Policy'] = "default-src 'self'"
            response.headers['X-Content-Type-Options'] = 'nosniff'
            response.headers['X-Frame-Options'] = 'DENY'
            response.headers['X-XSS-Protection'] = '1; mode=block'
            return response
```

#### Frontend

```javascript
// frontend/vite.config.js - Configuration production
export default defineConfig({
  plugins: [react()],
  build: {
    minify: 'terser',
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          ui: ['@radix-ui/react-button', '@radix-ui/react-card']
        }
      }
    }
  },
  server: {
    proxy: {
      '/api': {
        target: process.env.VITE_API_BASE_URL || 'http://localhost:5000',
        changeOrigin: true
      }
    }
  }
})
```

---

## 7. Bonnes Pratiques

### 7.1 Structure du Code

- **Séparation des responsabilités** : Modèles, Vues, Contrôleurs
- **Nommage cohérent** : snake_case (Python), camelCase (JavaScript)
- **Documentation** : Docstrings Python, JSDoc JavaScript
- **Tests** : Couverture minimale 80%

### 7.2 Sécurité

- **Validation des entrées** : Toujours valider côté backend
- **Authentification** : JWT ou sessions sécurisées
- **CORS** : Configuration restrictive en production
- **Logs** : Ne jamais logger de données sensibles

### 7.3 Performance

- **Cache** : Redis pour les données fréquemment accédées
- **Pagination** : Limiter les résultats des requêtes
- **Lazy loading** : Charger les composants à la demande
- **Optimisation des requêtes** : Index sur les colonnes fréquemment utilisées

---

## 8. Ressources et Aide

### 8.1 Documentation

- **Flask** : https://flask.palletsprojects.com/
- **React** : https://react.dev/
- **Tailwind CSS** : https://tailwindcss.com/
- **Radix UI** : https://www.radix-ui.com/

### 8.2 Outils de Développement

- **Postman** : Test des APIs
- **React DevTools** : Débogage React
- **SQLite Browser** : Visualisation de la base de données
- **VS Code Extensions** : Python, ES7+ React/Redux/React-Native snippets

### 8.3 Commandes Utiles

```bash
# Backend
python -m pytest backend/tests/  # Tests
python -m flake8 backend/src/    # Linting
python -m black backend/src/     # Formatage

# Frontend
npm test                         # Tests
npm run lint                     # Linting
npm run build                    # Build production

# Git
git add .
git commit -m "feat: nouvelle fonctionnalité"
git push origin main
```

Ce guide vous donne toutes les clés pour modifier et étendre l'application LMNP SAAS de manière autonome. N'hésitez pas à vous référer aux fichiers de documentation existants pour des détails spécifiques sur chaque composant.

