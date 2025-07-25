from flask import Blueprint, request, jsonify
import asyncio
from src.agents_ia_lmnp import (
    demander_agent_produit,
    demander_agent_dev,
    demander_agent_fiscal,
    chat_intelligent,
    orchestrateur
)

agents_bp = Blueprint('agents', __name__)

# ==========================================
# ROUTES AGENTS IA SPÉCIALISÉS
# ==========================================

@agents_bp.route('/agents/status', methods=['GET'])
def agents_status():
    """Vérifie le statut des agents IA"""
    return jsonify({
        'success': True,
        'agents': {
            'produit': {
                'nom': 'Chief Product Officer IA',
                'statut': 'operational',
                'expertise': ['UX Design', 'User Stories', 'MVP', 'Wireframing']
            },
            'developpeur': {
                'nom': 'Lead Developer Full Stack IA',
                'statut': 'operational', 
                'expertise': ['Python FastAPI', 'React TypeScript', 'PostgreSQL', 'Architecture']
            },
            'fiscal': {
                'nom': 'Expert-Comptable IA',
                'statut': 'operational',
                'expertise': ['Réglementation LMNP', 'Calculs fiscaux', 'CERFA 2031/2033', 'Optimisation']
            }
        },
        'orchestrateur': 'operational'
    })

@agents_bp.route('/agents/produit', methods=['POST'])
def consulter_agent_produit():
    """Consulte l'Agent Produit pour les spécifications UX"""
    data = request.get_json()
    demande = data.get('demande', '')
    contexte = data.get('contexte', {})
    
    if not demande:
        return jsonify({
            'success': False,
            'error': 'Demande requise'
        }), 400
    
    try:
        # Exécution synchrone pour Flask
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        reponse = loop.run_until_complete(demander_agent_produit(demande, contexte))
        loop.close()
        
        return jsonify({
            'success': True,
            'agent': 'produit',
            'reponse': reponse,
            'timestamp': '2024-07-25T10:00:00Z'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur Agent Produit: {str(e)}'
        }), 500

@agents_bp.route('/agents/developpeur', methods=['POST'])
def consulter_agent_dev():
    """Consulte l'Agent Développeur pour l'implémentation technique"""
    data = request.get_json()
    demande = data.get('demande', '')
    contexte = data.get('contexte', {})
    
    if not demande:
        return jsonify({
            'success': False,
            'error': 'Demande requise'
        }), 400
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        reponse = loop.run_until_complete(demander_agent_dev(demande, contexte))
        loop.close()
        
        return jsonify({
            'success': True,
            'agent': 'developpeur',
            'reponse': reponse,
            'timestamp': '2024-07-25T10:00:00Z'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur Agent Développeur: {str(e)}'
        }), 500

@agents_bp.route('/agents/fiscal', methods=['POST'])
def consulter_agent_fiscal():
    """Consulte l'Agent Fiscal pour les calculs et règles fiscales"""
    data = request.get_json()
    demande = data.get('demande', '')
    contexte = data.get('contexte', {})
    
    if not demande:
        return jsonify({
            'success': False,
            'error': 'Demande requise'
        }), 400
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        reponse = loop.run_until_complete(demander_agent_fiscal(demande, contexte))
        loop.close()
        
        return jsonify({
            'success': True,
            'agent': 'fiscal',
            'reponse': reponse,
            'timestamp': '2024-07-25T10:00:00Z'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur Agent Fiscal: {str(e)}'
        }), 500

@agents_bp.route('/agents/chat', methods=['POST'])
def chat_intelligent_route():
    """Chat intelligent qui route automatiquement vers les bons agents"""
    data = request.get_json()
    message = data.get('message', '')
    contexte = data.get('contexte', {})
    
    if not message:
        return jsonify({
            'success': False,
            'error': 'Message requis'
        }), 400
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        reponses = loop.run_until_complete(chat_intelligent(message, contexte))
        loop.close()
        
        # Détection des agents utilisés
        agents_detectes = orchestrateur.detect_agent_needed(message)
        
        return jsonify({
            'success': True,
            'message': message,
            'agents_consultes': [agent.value for agent in agents_detectes],
            'reponses': reponses,
            'timestamp': '2024-07-25T10:00:00Z'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur Chat Intelligent: {str(e)}'
        }), 500

# ==========================================
# ROUTES ASSISTANCE CONTEXTUELLE
# ==========================================

@agents_bp.route('/agents/assistance/onboarding', methods=['POST'])
def assistance_onboarding():
    """Assistance pour l'onboarding d'un nouvel utilisateur"""
    data = request.get_json()
    profil_utilisateur = data.get('profil', {})
    
    demande = f"""
    Crée un parcours d'onboarding personnalisé pour un utilisateur LMNP avec ce profil :
    - Expérience: {profil_utilisateur.get('experience', 'débutant')}
    - Nombre de biens: {profil_utilisateur.get('nombreBiens', 0)}
    - Type d'investissement: {profil_utilisateur.get('typeInvestissement', 'classique')}
    
    Génère un guide étape par étape adapté à son niveau.
    """
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        reponse = loop.run_until_complete(demander_agent_produit(demande, profil_utilisateur))
        loop.close()
        
        return jsonify({
            'success': True,
            'type': 'onboarding',
            'guide': reponse,
            'profil': profil_utilisateur
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur assistance onboarding: {str(e)}'
        }), 500

@agents_bp.route('/agents/assistance/calculs', methods=['POST'])
def assistance_calculs():
    """Assistance pour comprendre les calculs fiscaux"""
    data = request.get_json()
    type_calcul = data.get('type', '')
    donnees = data.get('donnees', {})
    
    demande = f"""
    Explique de manière simple le calcul {type_calcul} en LMNP avec ces données :
    {donnees}
    
    Fournis une explication pédagogique avec exemples concrets.
    """
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        reponse = loop.run_until_complete(demander_agent_fiscal(demande, donnees))
        loop.close()
        
        return jsonify({
            'success': True,
            'type': 'explication_calculs',
            'explication': reponse,
            'donnees': donnees
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur assistance calculs: {str(e)}'
        }), 500

@agents_bp.route('/agents/assistance/optimisation', methods=['POST'])
def assistance_optimisation():
    """Conseils d'optimisation fiscale personnalisés"""
    data = request.get_json()
    situation = data.get('situation', {})
    
    demande = f"""
    Analyse cette situation LMNP et propose des optimisations fiscales :
    - Recettes: {situation.get('recettes', 0)}€
    - Charges: {situation.get('charges', 0)}€
    - Nombre de biens: {situation.get('nombreBiens', 0)}
    - Régime actuel: {situation.get('regime', 'non défini')}
    
    Fournis des conseils concrets et chiffrés.
    """
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        reponse = loop.run_until_complete(demander_agent_fiscal(demande, situation))
        loop.close()
        
        return jsonify({
            'success': True,
            'type': 'optimisation',
            'conseils': reponse,
            'situation': situation
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur assistance optimisation: {str(e)}'
        }), 500

# ==========================================
# ROUTES GÉNÉRATION DE CONTENU
# ==========================================

@agents_bp.route('/agents/generer/user-stories', methods=['POST'])
def generer_user_stories():
    """Génère des user stories pour une fonctionnalité"""
    data = request.get_json()
    fonctionnalite = data.get('fonctionnalite', '')
    contexte = data.get('contexte', {})
    
    demande = f"""
    Génère des user stories détaillées pour la fonctionnalité : {fonctionnalite}
    
    Contexte : {contexte}
    
    Format : En tant que [utilisateur], je veux [action] afin de [bénéfice]
    Inclus les critères d'acceptation pour chaque story.
    """
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        reponse = loop.run_until_complete(demander_agent_produit(demande, contexte))
        loop.close()
        
        return jsonify({
            'success': True,
            'fonctionnalite': fonctionnalite,
            'user_stories': reponse
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur génération user stories: {str(e)}'
        }), 500

@agents_bp.route('/agents/generer/code', methods=['POST'])
def generer_code():
    """Génère du code selon les spécifications"""
    data = request.get_json()
    specifications = data.get('specifications', '')
    langage = data.get('langage', 'python')
    
    demande = f"""
    Génère du code {langage} selon ces spécifications :
    {specifications}
    
    Le code doit être prêt à l'emploi, documenté et suivre les bonnes pratiques.
    """
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        reponse = loop.run_until_complete(demander_agent_dev(demande, {'langage': langage}))
        loop.close()
        
        return jsonify({
            'success': True,
            'langage': langage,
            'code': reponse,
            'specifications': specifications
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur génération code: {str(e)}'
        }), 500

