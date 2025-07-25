#!/usr/bin/env python3
"""
Système d'Agents IA Spécialisés pour LMNP SAAS
Architecture avec 3 agents experts selon les spécifications
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
from openai import OpenAI
from datetime import datetime

# Configuration OpenAI
client = OpenAI(
    api_key=os.environ.get('OPENAI_API_KEY'),
    base_url=os.environ.get('OPENAI_API_BASE', 'https://api.openai.com/v1')
)

logger = logging.getLogger(__name__)

class AgentType(Enum):
    """Types d'agents IA spécialisés"""
    PRODUIT = "agentProduit"
    DEVELOPPEUR = "agentDev" 
    FISCAL = "agentFiscal"

@dataclass
class AgentResponse:
    """Réponse d'un agent IA"""
    agent_type: AgentType
    content: str
    confidence: float
    metadata: Dict[str, Any]
    timestamp: datetime

class AgentProduit:
    """
    🎯 Chief Product Officer IA - agentProduit
    
    Rôle : Traduire le besoin utilisateur en produit simple, utile et bien conçu
    Missions :
    - Définir les user stories (MVP puis roadmap)
    - Créer les wireframes et maquettes (avec Figma + prompts IA)
    - Structurer l'arborescence du produit et ses fonctionnalités
    - Créer le cahier des charges de chaque fonctionnalité
    """
    
    def __init__(self):
        self.agent_type = AgentType.PRODUIT
        self.expertise = [
            "User Experience Design",
            "Product Management", 
            "User Stories & MVP",
            "Wireframing & Prototyping",
            "Feature Specification",
            "LMNP User Journey"
        ]
        
    def get_system_prompt(self) -> str:
        return """Tu es le Chief Product Officer IA spécialisé dans les produits LMNP.

EXPERTISE :
- Conception de produits simples et efficaces ("less is more")
- Définition d'user stories et MVP pour investisseurs LMNP
- Création de wireframes et spécifications fonctionnelles
- Optimisation de l'expérience utilisateur pour la fiscalité

MISSION :
Traduire les besoins utilisateur en spécifications produit claires et actionables.

STYLE :
- Approche "less is more" : simplicité maximale
- Focus sur l'automatisation des calculs complexes
- Interface intuitive pour non-experts comptables
- Parcours guidé étape par étape

RÉPONSES :
- Spécifications fonctionnelles détaillées
- User stories avec critères d'acceptation
- Wireframes en format textuel
- Recommandations UX/UI"""

    def process_request(self, user_input: str, context: Dict[str, Any] = None) -> AgentResponse:
        """Traite une demande utilisateur et génère les spécifications produit"""
        try:
            messages = [
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": f"""
Contexte LMNP : {json.dumps(context or {}, indent=2)}

Demande utilisateur : {user_input}

Génère les spécifications produit pour répondre à ce besoin en suivant l'approche "less is more".
"""}
            ]
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.3,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            
            return AgentResponse(
                agent_type=self.agent_type,
                content=content,
                confidence=0.9,
                metadata={
                    "expertise_used": self.expertise,
                    "approach": "less_is_more",
                    "focus": "user_experience"
                },
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Erreur Agent Produit: {e}")
            return AgentResponse(
                agent_type=self.agent_type,
                content=f"Erreur lors du traitement: {str(e)}",
                confidence=0.0,
                metadata={"error": str(e)},
                timestamp=datetime.now()
            )

class AgentDeveloppeur:
    """
    ⚙️ Lead Developer Full Stack IA - agentDev
    
    Rôle : Développer le backend, frontend et APIs nécessaires
    Missions :
    - Maîtriser la stack technique (Python/FastAPI + PostgreSQL + React)
    - Choisir l'authentification, l'upload de docs, calculs d'amortissement, génération PDF/FEC
    - Gérer l'UX et l'identification, l'upload de docs, calculs d'amortissement, génération PDF/FEC
    - Maintenir une architecture scalable
    """
    
    def __init__(self):
        self.agent_type = AgentType.DEVELOPPEUR
        self.expertise = [
            "Python FastAPI Development",
            "React TypeScript Frontend",
            "PostgreSQL Database Design",
            "Authentication & Security",
            "PDF Generation & FEC",
            "Scalable Architecture"
        ]
        
    def get_system_prompt(self) -> str:
        return """Tu es le Lead Developer Full Stack IA spécialisé dans les applications LMNP.

STACK TECHNIQUE :
- Backend : Python FastAPI + SQLAlchemy + PostgreSQL
- Frontend : React 19 + TypeScript + Radix UI + Tailwind
- IA : OpenAI GPT-4 avec agents spécialisés
- Sécurité : JWT, chiffrement, RGPD

EXPERTISE :
- Architecture scalable et maintenable
- APIs RESTful avec documentation automatique
- Calculs fiscaux complexes et amortissements
- Génération PDF (liasses fiscales) et FEC
- Authentification sécurisée et gestion des sessions
- Interface utilisateur responsive et accessible

MISSION :
Implémenter les spécifications techniques avec les meilleures pratiques de développement.

RÉPONSES :
- Code Python/TypeScript prêt à l'emploi
- Architecture technique détaillée
- APIs documentées avec exemples
- Scripts de déploiement et configuration"""

    def process_request(self, user_input: str, context: Dict[str, Any] = None) -> AgentResponse:
        """Traite une demande de développement et génère le code/architecture"""
        try:
            messages = [
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": f"""
Spécifications techniques : {json.dumps(context or {}, indent=2)}

Demande de développement : {user_input}

Génère le code et l'architecture technique pour implémenter cette fonctionnalité.
"""}
            ]
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.2,
                max_tokens=3000
            )
            
            content = response.choices[0].message.content
            
            return AgentResponse(
                agent_type=self.agent_type,
                content=content,
                confidence=0.95,
                metadata={
                    "expertise_used": self.expertise,
                    "stack": "FastAPI_React_PostgreSQL",
                    "focus": "scalable_architecture"
                },
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Erreur Agent Développeur: {e}")
            return AgentResponse(
                agent_type=self.agent_type,
                content=f"Erreur lors du développement: {str(e)}",
                confidence=0.0,
                metadata={"error": str(e)},
                timestamp=datetime.now()
            )

class AgentFiscal:
    """
    📊 Expert-Comptable IA - agentFiscal
    
    Rôle : Fournir toute la logique fiscale, les formulaires CERFA, et les calculs conformes à la réglementation
    Missions :
    - Traduire les règles fiscales en formules (2031, 2033-A à G)
    - Valider les règles d'amortissement, les micro-BIC, TVA, etc.
    - Assurer la conformité réglementaire et les mises à jour fiscales
    """
    
    def __init__(self):
        self.agent_type = AgentType.FISCAL
        self.expertise = [
            "Réglementation LMNP 2024-2025",
            "Formulaires CERFA 2031/2033",
            "Calculs d'amortissements linéaires",
            "Optimisation micro-BIC vs régime réel",
            "Conformité fiscale française",
            "Génération liasses fiscales"
        ]
        
    def get_system_prompt(self) -> str:
        return """Tu es l'Expert-Comptable IA spécialisé dans la fiscalité LMNP.

EXPERTISE FISCALE :
- Réglementation LMNP en vigueur (2024-2025)
- Formulaires CERFA 2031 (bilan) et 2033 (compte de résultat)
- Calculs d'amortissements selon méthode linéaire
- Optimisation fiscale micro-BIC vs régime réel
- Règles de déductibilité des charges
- Prorata temporis et répartition terrain/construction

RÈGLES CLÉS :
- Amortissement linéaire : construction 20-25 ans, frais notaire/agence 15 ans
- Répartition standard : terrain 20% (non amortissable), construction 80%
- Micro-BIC : abattement 50% si recettes < 77 700€
- Régime réel : déduction charges réelles + amortissements

MISSION :
Fournir des calculs fiscaux précis et conformes à la réglementation française.

RÉPONSES :
- Formules de calcul détaillées
- Règles fiscales applicables
- Optimisations recommandées
- Validation de conformité"""

    def process_request(self, user_input: str, context: Dict[str, Any] = None) -> AgentResponse:
        """Traite une demande fiscale et génère les calculs/règles appropriés"""
        try:
            messages = [
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": f"""
Données fiscales : {json.dumps(context or {}, indent=2)}

Question fiscale : {user_input}

Fournis les calculs fiscaux précis et les règles applicables selon la réglementation LMNP.
"""}
            ]
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.1,
                max_tokens=2500
            )
            
            content = response.choices[0].message.content
            
            return AgentResponse(
                agent_type=self.agent_type,
                content=content,
                confidence=0.98,
                metadata={
                    "expertise_used": self.expertise,
                    "regulation": "LMNP_2024_2025",
                    "focus": "fiscal_compliance"
                },
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Erreur Agent Fiscal: {e}")
            return AgentResponse(
                agent_type=self.agent_type,
                content=f"Erreur lors du calcul fiscal: {str(e)}",
                confidence=0.0,
                metadata={"error": str(e)},
                timestamp=datetime.now()
            )

class OrchestrateursAgentsIA:
    """
    🎭 Orchestrateur des Agents IA Spécialisés
    
    Gère le routage intelligent des requêtes vers les agents appropriés
    et coordonne les réponses multi-agents pour des demandes complexes
    """
    
    def __init__(self):
        self.agents = {
            AgentType.PRODUIT: AgentProduit(),
            AgentType.DEVELOPPEUR: AgentDeveloppeur(),
            AgentType.FISCAL: AgentFiscal()
        }
        
    def detect_agent_needed(self, user_input: str) -> List[AgentType]:
        """Détecte quel(s) agent(s) sont nécessaires pour traiter la demande"""
        user_input_lower = user_input.lower()
        
        agents_needed = []
        
        # Mots-clés pour Agent Produit
        produit_keywords = [
            "user story", "wireframe", "ux", "ui", "interface", "parcours", 
            "expérience", "simple", "navigation", "étape", "workflow"
        ]
        
        # Mots-clés pour Agent Développeur  
        dev_keywords = [
            "code", "api", "backend", "frontend", "base de données", "architecture",
            "implémentation", "développement", "technique", "react", "python"
        ]
        
        # Mots-clés pour Agent Fiscal
        fiscal_keywords = [
            "amortissement", "fiscal", "cerfa", "2031", "2033", "micro-bic",
            "charges", "recettes", "calcul", "réglementation", "conformité"
        ]
        
        if any(keyword in user_input_lower for keyword in produit_keywords):
            agents_needed.append(AgentType.PRODUIT)
            
        if any(keyword in user_input_lower for keyword in dev_keywords):
            agents_needed.append(AgentType.DEVELOPPEUR)
            
        if any(keyword in user_input_lower for keyword in fiscal_keywords):
            agents_needed.append(AgentType.FISCAL)
            
        # Si aucun agent détecté, utiliser l'agent Produit par défaut
        if not agents_needed:
            agents_needed.append(AgentType.PRODUIT)
            
        return agents_needed
    
    async def process_request(self, user_input: str, context: Dict[str, Any] = None) -> List[AgentResponse]:
        """Traite une demande en routant vers les agents appropriés"""
        agents_needed = self.detect_agent_needed(user_input)
        responses = []
        
        for agent_type in agents_needed:
            agent = self.agents[agent_type]
            response = agent.process_request(user_input, context)
            responses.append(response)
            
        return responses
    
    async def get_agent_response(self, agent_type: AgentType, user_input: str, context: Dict[str, Any] = None) -> AgentResponse:
        """Obtient une réponse d'un agent spécifique"""
        if agent_type not in self.agents:
            raise ValueError(f"Agent type {agent_type} not found")
            
        agent = self.agents[agent_type]
        return agent.process_request(user_input, context)

# Instance globale de l'orchestrateur
orchestrateur = OrchestrateursAgentsIA()

# Fonctions utilitaires pour l'utilisation dans l'application
async def demander_agent_produit(demande: str, contexte: Dict = None) -> str:
    """Demande à l'Agent Produit de définir les spécifications"""
    response = await orchestrateur.get_agent_response(AgentType.PRODUIT, demande, contexte)
    return response.content

async def demander_agent_dev(demande: str, contexte: Dict = None) -> str:
    """Demande à l'Agent Développeur d'implémenter une fonctionnalité"""
    response = await orchestrateur.get_agent_response(AgentType.DEVELOPPEUR, demande, contexte)
    return response.content

async def demander_agent_fiscal(demande: str, contexte: Dict = None) -> str:
    """Demande à l'Agent Fiscal de calculer ou valider des règles fiscales"""
    response = await orchestrateur.get_agent_response(AgentType.FISCAL, demande, contexte)
    return response.content

async def chat_intelligent(message: str, contexte: Dict = None) -> List[str]:
    """Chat intelligent qui route automatiquement vers les bons agents"""
    responses = await orchestrateur.process_request(message, contexte)
    return [response.content for response in responses]

