# Agents IA et Services Métier - LMNP SAAS

Ce document détaille l'architecture des agents d'intelligence artificielle et des services métier de l'application LMNP SAAS.

---

## 1. Vue d'ensemble du système d'IA

L'application LMNP SAAS intègre un système d'agents IA spécialisés qui automatisent et optimisent les tâches fiscales et comptables. Le système est basé sur :

- **OpenAI GPT-4** : Modèle de langage pour le traitement conversationnel
- **Orchestrateur intelligent** : Routage automatique vers l'agent approprié
- **Agents spécialisés** : Chaque agent a une expertise métier spécifique
- **Base de connaissances** : Réglementation fiscale LMNP intégrée

### Architecture générale

```
Utilisateur
    ↓
Orchestrateur IA
    ↓
┌─────────────┬─────────────┬─────────────┐
│Agent Accueil│Agent Fiscal │Agent Comptable│
└─────────────┴─────────────┴─────────────┘
    ↓               ↓               ↓
Services Métier  Expertise    Catégorisation
                Fiscale         ML
```

---

## 2. Classe de Base : `BaseAgentSimple`

Tous les agents héritent de cette classe abstraite qui fournit :

### 2.1 Structure commune

```python
class BaseAgentSimple(ABC):
    def __init__(self, name: str, description: str, temperature: float = 0.7):
        self.name = name
        self.description = description
        self.temperature = temperature
        self.client = openai.OpenAI()
        self.conversation_history = []
```

### 2.2 Méthodes abstraites

- **`_get_system_prompt()`** : Définit la personnalité et les instructions de l'agent
- **`_process_tools()`** : Traite les outils spécifiques à chaque agent

### 2.3 Fonctionnalités communes

- **Gestion de l'historique** : Conservation des 3 derniers échanges
- **Gestion d'erreurs** : Réponses gracieuses en cas d'erreur
- **Réponses standardisées** : Format `AgentResponse` uniforme

```python
@dataclass
class AgentResponse:
    agent_name: str
    message: str
    data: Optional[Dict] = None
    actions_suggested: Optional[List[str]] = None
    confidence: float = 1.0
    timestamp: datetime = None
```

---

## 3. Agent Accueil (`AgentAccueilSimple`)

### 3.1 Rôle et responsabilités

L'Agent Accueil est spécialisé dans :
- **Onboarding personnalisé** des nouveaux utilisateurs
- **Identification du profil** utilisateur (débutant/expérimenté/professionnel)
- **Création de parcours** d'accompagnement adaptés
- **Explication des concepts** LMNP de base

### 3.2 Profils utilisateur gérés

```python
profils_utilisateur = {
    'debutant': {
        'description': 'Première expérience en location meublée',
        'besoins': ['Formation de base', 'Guide pas à pas', 'Explications simples'],
        'parcours': ['Comprendre LMNP', 'Ajouter premier bien', 'Première déclaration']
    },
    'experimente': {
        'description': 'Quelques années d\'expérience LMNP',
        'besoins': ['Optimisation fiscale', 'Automatisation', 'Conseils avancés'],
        'parcours': ['Import données', 'Optimisation régime', 'Déclarations multiples']
    },
    'professionnel': {
        'description': 'Gestionnaire ou investisseur expérimenté',
        'besoins': ['Efficacité maximale', 'Reporting avancé', 'Intégrations'],
        'parcours': ['Configuration avancée', 'Automatisation complète', 'Tableaux de bord']
    }
}
```

### 3.3 Fonctionnalités principales

#### **Génération de parcours d'onboarding**

```python
def _generer_parcours_onboarding(self, profil: str) -> Dict:
    parcours = {
        'profil': profil,
        'etapes': [
            {
                'numero': 1,
                'titre': 'Configuration du profil',
                'description': 'Renseigner vos informations personnelles et fiscales',
                'duree_estimee': '5 minutes',
                'actions': ['Compléter profil utilisateur', 'Définir date début activité']
            },
            # ... autres étapes
        ],
        'duree_totale': '55 minutes'
    }
    return parcours
```

#### **Explication des concepts LMNP**

L'agent peut expliquer :
- **LMNP** : Définition, avantages, conditions
- **Micro-BIC** : Régime simplifié, seuils, abattements
- **Régime réel** : Déductions, amortissements, obligations
- **Amortissements** : Calcul, limitation article 39C

### 3.4 Exemple d'utilisation

```python
agent_accueil = AgentAccueilSimple()
response = agent_accueil.process_message(
    "Bonjour, je suis nouveau dans la location meublée",
    context={}
)
# Retourne un parcours personnalisé et des explications adaptées
```

---

## 4. Agent Fiscal (`AgentFiscalSimple`)

### 4.1 Rôle et responsabilités

L'Agent Fiscal est l'expert en réglementation fiscale LMNP :
- **Calculs fiscaux automatiques** (micro-BIC vs régime réel)
- **Optimisation fiscale** personnalisée
- **Conseil réglementaire** basé sur la législation actuelle
- **Génération de recommandations** fiscales

### 4.2 Base de connaissances intégrée

```python
knowledge_base = {
    'reglements': [
        "Le régime LMNP permet de déduire les amortissements selon l'article 39C du CGI",
        "Les seuils micro-BIC 2024: longue durée 77700€, tourisme classé 77700€, tourisme non classé 15000€",
        "La limitation article 39C: amortissements déductibles limités au résultat avant amortissement"
    ],
    'seuils_2024': {
        'micro_bic': {
            'longue_duree': 77700,
            'tourisme_classe': 77700,
            'tourisme_non_classe': 15000
        }
    },
    'taux_amortissement': {
        'immeuble': 0.033,  # 30 ans
        'mobilier': 0.10    # 10 ans
    }
}
```

### 4.3 Fonctionnalités principales

#### **Optimisation fiscale automatique**

```python
def _optimiser_regime_fiscal(self, donnees_fiscales: Dict) -> Dict:
    recettes = donnees_fiscales['recettes']
    charges = donnees_fiscales['charges']
    type_location = donnees_fiscales['type_location']
    
    # Calcul micro-BIC
    seuil = self.knowledge_base['seuils_2024']['micro_bic'][type_location]
    eligible_micro = recettes <= seuil
    
    if eligible_micro:
        abattement = 0.5 if type_location == 'longue_duree' else 0.71
        base_imposable_micro = recettes * (1 - abattement)
    
    # Calcul régime réel
    benefice_reel = max(0, recettes - charges)
    
    # Recommandation
    regime_optimal = 'micro_bic' if eligible_micro and base_imposable_micro < benefice_reel else 'reel'
    
    return {
        'regime_recommande': regime_optimal,
        'economie_estimee': abs(base_imposable_micro - benefice_reel),
        'details_calculs': {...}
    }
```

#### **Conseil réglementaire contextuel**

L'agent utilise sa base de connaissances pour fournir des conseils précis selon :
- Le type de location (longue durée, tourisme classé/non classé)
- Les montants de recettes et charges
- La situation patrimoniale de l'utilisateur

### 4.4 Intégration avec l'expertise fiscale

L'Agent Fiscal utilise la classe `ExpertiseFiscaleLMNP` pour les calculs complexes :

```python
def _process_tools(self, message: str, context: Optional[Dict] = None) -> Dict:
    if 'optimisation' in message.lower():
        # Utilisation du moteur d'expertise fiscale
        calculs = self.expert_fiscal.calculer_optimisation_fiscale(
            recettes=context['recettes'],
            charges=context['charges'],
            type_location=context['type_location']
        )
        return {'optimisation_fiscale': calculs}
```

---

## 5. Agent Comptable (`AgentComptableSimple`)

### 5.1 Rôle et responsabilités

L'Agent Comptable automatise la gestion comptable :
- **Catégorisation automatique** des transactions avec ML
- **Analyse des flux financiers** et détection de tendances
- **Détection d'anomalies** comptables
- **Génération de rapports** comptables détaillés

### 5.2 Système de catégorisation ML

#### **Base de patterns de reconnaissance**

```python
categorisation_patterns = {
    'recettes': {
        'loyers': {
            'compte': '706000',
            'patterns': ['loyer', 'rent', 'location', 'bail'],
            'confidence_base': 0.95
        }
    },
    'charges': {
        'electricite': {
            'compte': '606100',
            'patterns': ['edf', 'engie', 'électricité', 'electric'],
            'confidence_base': 0.95
        },
        'travaux': {
            'compte': '615000',
            'patterns': ['travaux', 'réparation', 'maintenance', 'plombier'],
            'confidence_base': 0.85
        }
    }
}
```

#### **Algorithme de catégorisation**

```python
def _categoriser_transaction(self, transaction_data: Dict) -> Dict:
    libelle = transaction_data.get('libelle', '').lower()
    montant = float(transaction_data.get('montant', 0))
    
    # Détermination du type (recette/charge)
    type_transaction = 'recette' if montant > 0 else 'charge'
    
    # Recherche de patterns
    meilleur_match = None
    meilleur_score = 0
    
    patterns = self.categorisation_patterns[type_transaction + 's']
    
    for categorie, data in patterns.items():
        score = sum(1 for pattern in data['patterns'] if pattern in libelle)
        if score > meilleur_score:
            meilleur_score = score
            meilleur_match = {
                'categorie': categorie,
                'compte_comptable': data['compte'],
                'confiance': data['confidence_base'] * (score / len(data['patterns']))
            }
    
    return meilleur_match or {
        'categorie': 'non_categorise',
        'compte_comptable': '708500',
        'confiance': 0.1
    }
```

### 5.3 Analyse financière avancée

#### **Génération de rapports comptables**

```python
def _generer_rapport_comptable(self, transactions: List, periode: str) -> Dict:
    # Calculs des totaux
    total_recettes = sum(t['montant'] for t in transactions if t['montant'] > 0)
    total_charges = sum(abs(t['montant']) for t in transactions if t['montant'] < 0)
    resultat = total_recettes - total_charges
    
    # Répartition par catégories
    repartition = {}
    for transaction in transactions:
        categorie = self._quick_categorize(transaction['libelle'], transaction['montant'])
        repartition[categorie] = repartition.get(categorie, 0) + abs(transaction['montant'])
    
    # Indicateurs de performance
    indicateurs = {
        'rentabilite_brute': round((resultat / total_recettes * 100), 2) if total_recettes > 0 else 0,
        'ratio_charges': round((total_charges / total_recettes * 100), 2) if total_recettes > 0 else 0,
        'ticket_moyen_recette': round(total_recettes / len([t for t in transactions if t['montant'] > 0]), 2)
    }
    
    return {
        'periode': periode,
        'resume_executif': {
            'total_recettes': round(total_recettes, 2),
            'total_charges': round(total_charges, 2),
            'resultat_net': round(resultat, 2),
            'nombre_transactions': len(transactions),
            'rentabilite': f"{indicateurs['rentabilite_brute']}%"
        },
        'indicateurs_performance': indicateurs,
        'repartition_charges': repartition
    }
```

#### **Détection d'anomalies**

L'agent peut détecter :
- **Transactions atypiques** (montants inhabituels)
- **Doublons potentiels** (même libellé, même montant, dates proches)
- **Catégorisations douteuses** (faible niveau de confiance)
- **Déséquilibres** dans les ratios financiers

---

## 6. Orchestrateur (`OrchestrateurAgentsSimple`)

### 6.1 Rôle central

L'Orchestrateur coordonne tous les agents et :
- **Route automatiquement** les demandes vers l'agent approprié
- **Maintient l'historique** des conversations
- **Gère le contexte** entre les agents
- **Fournit une interface unifiée** pour l'API

### 6.2 Sélection automatique d'agent

```python
def _select_best_agent(self, message: str, context: Dict = None) -> str:
    message_lower = message.lower()
    
    # Mots-clés pour chaque agent
    keywords = {
        'accueil': ['bonjour', 'aide', 'commencer', 'débuter', 'nouveau', 'guide'],
        'fiscal': ['impôt', 'fiscal', 'régime', 'micro-bic', 'réel', 'amortissement'],
        'comptable': ['transaction', 'catégorie', 'charge', 'recette', 'comptabilité']
    }
    
    # Calcul des scores
    scores = {}
    for agent_name, agent_keywords in keywords.items():
        score = sum(1 for keyword in agent_keywords if keyword in message_lower)
        scores[agent_name] = score
    
    # Sélection du meilleur agent
    best_agent = max(scores, key=scores.get)
    return best_agent if scores[best_agent] > 0 else 'accueil'
```

### 6.3 Interface API

```python
def process_user_message(self, message: str, agent_name: str = None, context: Dict = None) -> AgentResponse:
    # Sélection automatique si agent non spécifié
    if agent_name is None:
        agent_name = self._select_best_agent(message, context)
    
    # Traitement par l'agent sélectionné
    agent = self.agents[agent_name]
    response = agent.process_message(message, context)
    
    # Sauvegarde dans l'historique
    self.conversation_history.append({
        'timestamp': datetime.now(),
        'user_message': message,
        'agent_used': agent_name,
        'agent_response': response.message,
        'context': context
    })
    
    return response
```

---

## 7. Service d'Expertise Fiscale (`ExpertiseFiscaleLMNP`)

### 7.1 Moteur de calculs fiscaux

Ce service implémente tous les calculs fiscaux LMNP conformes à la réglementation française.

#### **Structures de données**

```python
@dataclass
class SeuilsFiscaux:
    annee: int
    micro_bic_longue_duree: Decimal
    micro_bic_tourisme_classe: Decimal
    micro_bic_tourisme_non_classe: Decimal
    abattement_longue_duree: Decimal
    abattement_tourisme_classe: Decimal

@dataclass
class BienImmobilier:
    id: str
    adresse: str
    type_location: TypeLocation
    date_acquisition: datetime.date
    prix_acquisition: Decimal
    frais_notaire: Decimal
    valeur_terrain: Decimal
    valeur_mobilier: Decimal
    
    @property
    def base_amortissable_immeuble(self) -> Decimal:
        return self.prix_acquisition + self.frais_notaire - self.valeur_terrain
```

### 7.2 Calculs implémentés

- **Régime micro-BIC** : Calcul avec abattements selon le type de location
- **Régime réel** : Déduction des charges réelles et amortissements
- **Amortissements** : Calcul selon les durées légales (30 ans immeuble, 10 ans mobilier)
- **Limitation article 39C** : Application de la limitation des amortissements
- **Optimisation fiscale** : Comparaison automatique des régimes

### 7.3 Seuils 2024-2025

```python
seuils_2025 = SeuilsFiscaux(
    annee=2025,
    micro_bic_longue_duree=Decimal('77700'),
    micro_bic_tourisme_classe=Decimal('77700'),
    micro_bic_tourisme_non_classe=Decimal('15000'),
    micro_bic_chambre_hotes=Decimal('77700'),
    abattement_longue_duree=Decimal('0.50'),    # 50%
    abattement_tourisme_classe=Decimal('0.71'),  # 71%
    abattement_tourisme_non_classe=Decimal('0.50'), # 50%
    abattement_chambre_hotes=Decimal('0.71')    # 71%
)
```

---

## 8. Intégration avec l'API

### 8.1 Endpoints disponibles

Les agents IA sont accessibles via l'API REST :

- **`GET /api/agents/agents`** : Liste des agents disponibles
- **`POST /api/agents/chat`** : Chat conversationnel avec routage automatique
- **`POST /api/agents/analyze-transaction`** : Analyse de transaction par l'Agent Comptable
- **`POST /api/agents/optimize-fiscal`** : Optimisation fiscale par l'Agent Fiscal

### 8.2 Exemple d'utilisation API

```javascript
// Chat avec routage automatique
const response = await fetch('/api/agents/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        message: "Comment optimiser ma fiscalité LMNP ?",
        contexte: {
            recettes: 25000,
            charges: 8000,
            type_location: "longue_duree"
        }
    })
});

const result = await response.json();
// {
//   "response": "Analyse détaillée de votre situation...",
//   "agent_utilise": "fiscal",
//   "confiance": 0.9,
//   "actions_suggerees": ["Consulter régime réel", "Calculer amortissements"]
// }
```

### 8.3 Gestion des erreurs

```python
try:
    reponse = orchestrateur.traiter_demande(message, contexte)
    return jsonify({
        'response': reponse.get('reponse', 'Réponse non disponible'),
        'agent_utilise': reponse.get('agent_utilise', 'unknown'),
        'confiance': reponse.get('confiance', 0.0)
    })
except Exception as e:
    return jsonify({
        'response': f"Erreur lors du traitement: {str(e)}",
        'agent_utilise': 'error',
        'confiance': 0.0
    })
```

---

## 9. Configuration et Déploiement

### 9.1 Variables d'environnement requises

```bash
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_API_BASE=https://api.openai.com/v1  # Optionnel
```

### 9.2 Initialisation des services

```python
# Dans main.py
try:
    from src.services.agents_ia_simple_lmnp import OrchestrateurAgents
    orchestrateur = OrchestrateurAgents()
    agents_available = True
except ImportError:
    agents_available = False

# Dans les routes
if not agents_available:
    return jsonify({
        'response': "Les agents IA ne sont pas disponibles actuellement.",
        'agent_utilise': 'system',
        'confiance': 0.0
    })
```

### 9.3 Monitoring et logs

```python
import logging

logger = logging.getLogger(__name__)

# Logs automatiques dans chaque agent
logger.info(f"Agent {self.name} traite: {message[:100]}...")
logger.error(f"Erreur agent {self.name}: {e}")
```

---

## 10. Évolutions futures

### 10.1 Améliorations prévues

- **Fine-tuning** des modèles sur les données LMNP spécifiques
- **Agent OCR** pour l'extraction automatique de documents
- **Agent Déclaration** pour la génération automatique des formulaires CERFA
- **Apprentissage continu** basé sur les retours utilisateurs

### 10.2 Intégrations possibles

- **APIs externes** : DGFiP, cadastre, banques
- **Outils comptables** : Export vers logiciels de comptabilité
- **Services cloud** : Stockage sécurisé des documents

### 10.3 Optimisations techniques

- **Cache intelligent** pour les calculs récurrents
- **Parallélisation** des traitements pour les gros volumes
- **Modèles locaux** pour réduire les coûts API

Le système d'agents IA de LMNP SAAS offre une **automatisation intelligente** des tâches fiscales et comptables, avec une **expertise métier intégrée** et une **interface conversationnelle** naturelle pour l'utilisateur.

