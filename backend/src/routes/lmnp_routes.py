from flask import Blueprint, request, jsonify
from datetime import datetime, date
import json
from src.expertise_fiscale_lmnp import (
    calculer_amortissement_bien,
    calculer_resultat_fiscal,
    optimiser_regime,
    expert_fiscal
)

lmnp_bp = Blueprint('lmnp', __name__)

# ==========================================
# ROUTES DÉCLARATIONS LMNP
# ==========================================

@lmnp_bp.route('/declarations', methods=['GET'])
def get_declarations():
    """Récupère toutes les déclarations de l'utilisateur"""
    # Simulation de données pour la demo
    declarations = [
        {
            'id': 1,
            'annee': 2024,
            'statut': 'en_cours',
            'progression': 65,
            'biens': 2,
            'recettes': 24000,
            'resultat': 3200,
            'dateModification': '2024-07-20',
            'teletransmise': False
        },
        {
            'id': 2,
            'annee': 2023,
            'statut': 'complete',
            'progression': 100,
            'biens': 1,
            'recettes': 18000,
            'resultat': 2100,
            'dateModification': '2024-03-15',
            'teletransmise': True
        }
    ]
    
    return jsonify({
        'success': True,
        'declarations': declarations,
        'total': len(declarations)
    })

@lmnp_bp.route('/declarations', methods=['POST'])
def create_declaration():
    """Crée une nouvelle déclaration LMNP"""
    data = request.get_json()
    
    nouvelle_declaration = {
        'id': 3,  # Simulation d'un nouvel ID
        'annee': data.get('annee', datetime.now().year),
        'statut': 'brouillon',
        'progression': 0,
        'biens': 0,
        'recettes': 0,
        'resultat': 0,
        'dateCreation': datetime.now().isoformat(),
        'dateModification': datetime.now().isoformat(),
        'teletransmise': False
    }
    
    return jsonify({
        'success': True,
        'declaration': nouvelle_declaration,
        'message': 'Déclaration créée avec succès'
    }), 201

@lmnp_bp.route('/declarations/<int:declaration_id>', methods=['GET'])
def get_declaration(declaration_id):
    """Récupère une déclaration spécifique"""
    # Simulation de données
    declaration = {
        'id': declaration_id,
        'annee': 2024,
        'statut': 'en_cours',
        'progression': 65,
        'biens': [
            {
                'id': 1,
                'adresse': '123 Rue de la Paix, 75001 Paris',
                'dateEntreeLmnp': '2024-01-01',
                'prixAcquisition': 200000,
                'fraisNotaire': 15000,
                'fraisAgence': 5000,
                'recettes': {
                    'loyersBruts': 24000,
                    'autresRecettes': 0
                },
                'depenses': {
                    'fraisGestion': 2400,
                    'chargesCopropriete': 3600,
                    'assurances': 800,
                    'taxeFonciere': 1200
                },
                'emprunt': {
                    'interetsAnnuels': 4800,
                    'assuranceEmprunt': 600
                }
            }
        ]
    }
    
    return jsonify({
        'success': True,
        'declaration': declaration
    })

# ==========================================
# ROUTES BIENS IMMOBILIERS
# ==========================================

@lmnp_bp.route('/biens', methods=['POST'])
def create_bien():
    """Ajoute un nouveau bien immobilier"""
    data = request.get_json()
    
    # Validation des données
    required_fields = ['adresse', 'dateEntreeLmnp', 'prixAcquisition']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'success': False,
                'error': f'Champ requis manquant: {field}'
            }), 400
    
    # Suggestion de répartition terrain/construction selon localisation
    code_postal = data.get('codePostal', '')
    part_terrain, part_construction = expert_fiscal.suggerer_repartition_par_localisation(code_postal)
    
    nouveau_bien = {
        'id': len(data.get('biens_existants', [])) + 1,
        'adresse': data['adresse'],
        'dateEntreeLmnp': data['dateEntreeLmnp'],
        'prixAcquisition': data['prixAcquisition'],
        'fraisNotaire': data.get('fraisNotaire', 0),
        'fraisAgence': data.get('fraisAgence', 0),
        'partTerrain': float(part_terrain),
        'partConstruction': float(part_construction),
        'dureeAmortissementConstruction': 25,
        'dureeAmortissementFrais': 15,
        'creditBancaire': data.get('creditBancaire', False)
    }
    
    return jsonify({
        'success': True,
        'bien': nouveau_bien,
        'suggestions': {
            'partTerrain': float(part_terrain),
            'partConstruction': float(part_construction),
            'message': f'Répartition suggérée pour {code_postal}: {int(part_terrain*100)}% terrain, {int(part_construction*100)}% construction'
        }
    }), 201

@lmnp_bp.route('/biens/<int:bien_id>/recettes', methods=['PUT'])
def update_recettes(bien_id):
    """Met à jour les recettes d'un bien"""
    data = request.get_json()
    
    recettes = {
        'loyersBruts': data.get('loyersBruts', 0),
        'autresRecettes': data.get('autresRecettes', 0),
        'total': data.get('loyersBruts', 0) + data.get('autresRecettes', 0)
    }
    
    return jsonify({
        'success': True,
        'recettes': recettes,
        'message': 'Recettes mises à jour avec succès'
    })

@lmnp_bp.route('/biens/<int:bien_id>/depenses', methods=['PUT'])
def update_depenses(bien_id):
    """Met à jour les dépenses d'un bien"""
    data = request.get_json()
    
    # Calcul du total des dépenses
    total_depenses = sum([
        data.get('fraisGestion', 0),
        data.get('chargesCopropriete', 0),
        data.get('assurances', 0),
        data.get('fraisMenageEntretien', 0),
        data.get('fraisPlateformes', 0),
        data.get('fraisComptabilite', 0),
        data.get('abonnements', 0),
        data.get('taxeFonciere', 0),
        data.get('taxeHabitation', 0),
        data.get('taxeSejour', 0),
        data.get('cfe', 0),
        data.get('chargesSociales', 0),
        data.get('depensesDiverses', 0),
        data.get('petitsTravaux', 0),
        data.get('petitsMeubles', 0)
    ])
    
    depenses = {**data, 'total': total_depenses}
    
    return jsonify({
        'success': True,
        'depenses': depenses,
        'message': 'Dépenses mises à jour avec succès'
    })

# ==========================================
# ROUTES CALCULS FISCAUX
# ==========================================

@lmnp_bp.route('/calculs/amortissements', methods=['POST'])
def calculer_amortissements():
    """Calcule les amortissements d'un bien"""
    data = request.get_json()
    
    try:
        # Conversion de la date
        if isinstance(data.get('date_entree_lmnp'), str):
            data['date_entree_lmnp'] = datetime.strptime(data['date_entree_lmnp'], '%Y-%m-%d').date()
        
        amortissements = calculer_amortissement_bien(data, data.get('annee', datetime.now().year))
        
        return jsonify({
            'success': True,
            'amortissements': amortissements,
            'details': {
                'methode': 'linéaire',
                'dureeConstruction': data.get('duree_amortissement_construction', 25),
                'dureeFrais': data.get('duree_amortissement_frais', 15),
                'prorataTemporisPremièreAnnee': True
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur calcul amortissements: {str(e)}'
        }), 400

@lmnp_bp.route('/calculs/resultat', methods=['POST'])
def calculer_resultat():
    """Calcule le résultat fiscal d'un bien"""
    data = request.get_json()
    
    try:
        bien_data = data.get('bien', {})
        recettes_data = data.get('recettes', {})
        depenses_data = data.get('depenses', {})
        emprunt_data = data.get('emprunt')
        
        # Conversion de la date
        if isinstance(bien_data.get('date_entree_lmnp'), str):
            bien_data['date_entree_lmnp'] = datetime.strptime(bien_data['date_entree_lmnp'], '%Y-%m-%d').date()
        
        resultat = calculer_resultat_fiscal(bien_data, recettes_data, depenses_data, emprunt_data)
        
        return jsonify({
            'success': True,
            'resultat': resultat
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur calcul résultat: {str(e)}'
        }), 400

@lmnp_bp.route('/calculs/optimisation', methods=['POST'])
def optimiser_regime_fiscal():
    """Compare micro-BIC vs régime réel"""
    data = request.get_json()
    
    try:
        recettes_totales = data.get('recettesTotales', 0)
        charges_totales = data.get('chargesTotales', 0)
        
        optimisation = optimiser_regime(recettes_totales, charges_totales)
        
        return jsonify({
            'success': True,
            'optimisation': optimisation,
            'conseils': expert_fiscal.generer_conseils_optimisation({
                'recettes_totales': recettes_totales,
                'depenses_totales': charges_totales,
                'resultat_apres_amortissement': recettes_totales - charges_totales
            })
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur optimisation: {str(e)}'
        }), 400

@lmnp_bp.route('/calculs/cfe', methods=['POST'])
def estimer_cfe():
    """Estime la CFE selon les recettes"""
    data = request.get_json()
    
    try:
        recettes = data.get('recettes', 0)
        commune = data.get('commune', '')
        
        cfe_estimee = expert_fiscal.calculer_cfe_estimee(recettes, commune)
        
        return jsonify({
            'success': True,
            'cfe_estimee': float(cfe_estimee),
            'base_minimum': 227,
            'note': 'Estimation basée sur les recettes déclarées'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur estimation CFE: {str(e)}'
        }), 400

# ==========================================
# ROUTES LIASSES FISCALES
# ==========================================

@lmnp_bp.route('/liasses/generer', methods=['POST'])
def generer_liasse():
    """Génère les formulaires CERFA 2031/2033"""
    data = request.get_json()
    
    # Simulation de génération de liasse
    liasse = {
        'formulaires': ['2031', '2033-A', '2033-B', '2033-C'],
        'statut': 'generee',
        'dateGeneration': datetime.now().isoformat(),
        'urlTelechargement': '/api/liasses/download/123',
        'validite': '30 jours'
    }
    
    return jsonify({
        'success': True,
        'liasse': liasse,
        'message': 'Liasse fiscale générée avec succès'
    })

@lmnp_bp.route('/liasses/teletransmettre', methods=['POST'])
def teletransmettre():
    """Télétransmet la déclaration à la DGFiP"""
    data = request.get_json()
    
    # Simulation de télétransmission
    transmission = {
        'statut': 'transmise',
        'numeroAccuse': 'LMNP2024-' + str(datetime.now().timestamp()).replace('.', ''),
        'dateTransmission': datetime.now().isoformat(),
        'delaiTraitement': '48-72 heures'
    }
    
    return jsonify({
        'success': True,
        'transmission': transmission,
        'message': 'Déclaration télétransmise avec succès'
    })

# ==========================================
# ROUTES STATISTIQUES
# ==========================================

@lmnp_bp.route('/stats/dashboard', methods=['GET'])
def get_dashboard_stats():
    """Récupère les statistiques pour le dashboard"""
    stats = {
        'totalBiens': 3,
        'recettesAnnuelles': 24000,
        'economiesFiscales': 8500,
        'declarationsCompletes': 1,
        'optimisationPossible': {
            'regime': 'reel',
            'economie': 1200,
            'conseil': 'Le régime réel vous ferait économiser 1 200€ supplémentaires'
        }
    }
    
    return jsonify({
        'success': True,
        'stats': stats
    })

