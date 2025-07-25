#!/usr/bin/env python3
"""
Module d'Expertise Fiscale LMNP
Implémente toutes les règles fiscales et calculs pour les locations meublées non professionnelles
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, date
from decimal import Decimal, ROUND_HALF_UP
import logging

logger = logging.getLogger(__name__)

@dataclass
class BienImmobilier:
    """Représente un bien immobilier LMNP"""
    id: int
    adresse: str
    date_entree_lmnp: date
    prix_acquisition: Decimal
    frais_notaire: Decimal
    frais_agence: Decimal
    part_terrain: Decimal = Decimal('0.20')  # 20% par défaut
    part_construction: Decimal = Decimal('0.80')  # 80% par défaut
    duree_amortissement_construction: int = 25  # années
    duree_amortissement_frais: int = 15  # années
    
@dataclass
class Recettes:
    """Recettes d'un bien LMNP"""
    loyers_bruts: Decimal
    autres_recettes: Decimal = Decimal('0')
    
@dataclass
class Depenses:
    """Dépenses d'un bien LMNP"""
    frais_gestion: Decimal = Decimal('0')
    charges_copropriete: Decimal = Decimal('0')
    assurances: Decimal = Decimal('0')
    frais_menage_entretien: Decimal = Decimal('0')
    frais_plateformes: Decimal = Decimal('0')
    frais_comptabilite: Decimal = Decimal('0')
    abonnements: Decimal = Decimal('0')
    taxes_fonciere: Decimal = Decimal('0')
    taxes_habitation: Decimal = Decimal('0')
    taxe_sejour: Decimal = Decimal('0')
    cfe: Decimal = Decimal('0')
    charges_sociales: Decimal = Decimal('0')
    depenses_diverses: Decimal = Decimal('0')
    petits_travaux: Decimal = Decimal('0')
    petits_meubles: Decimal = Decimal('0')
    
@dataclass
class Emprunt:
    """Informations sur l'emprunt d'un bien"""
    interets_annuels: Decimal
    assurance_emprunt: Decimal = Decimal('0')
    frais_dossier: Decimal = Decimal('0')
    frais_courtier: Decimal = Decimal('0')
    
@dataclass
class Amortissement:
    """Calcul des amortissements d'un bien"""
    construction_annuel: Decimal
    construction_prorata: Decimal
    frais_notaire_annuel: Decimal
    frais_notaire_prorata: Decimal
    frais_agence_annuel: Decimal
    frais_agence_prorata: Decimal
    total_annuel: Decimal
    total_prorata: Decimal

class ExpertiseFiscaleLMNP:
    """
    Expert-comptable virtuel spécialisé dans la fiscalité LMNP
    Implémente toutes les règles fiscales françaises en vigueur
    """
    
    # Seuils fiscaux 2024-2025
    SEUIL_MICRO_BIC = Decimal('77700')  # Seuil micro-BIC
    ABATTEMENT_MICRO_BIC = Decimal('0.50')  # 50% d'abattement
    
    def __init__(self):
        self.annee_fiscale = datetime.now().year
        
    def calculer_amortissement(self, bien: BienImmobilier, annee: int) -> Amortissement:
        """
        Calcule les amortissements d'un bien selon la méthode linéaire
        avec prorata temporis pour la première année
        """
        try:
            # Calcul du prorata temporis pour la première année
            if annee == bien.date_entree_lmnp.year:
                jours_restants = (date(annee, 12, 31) - bien.date_entree_lmnp).days + 1
                prorata = Decimal(jours_restants) / Decimal(365)
            else:
                prorata = Decimal('1')
            
            # Base amortissable construction (hors terrain)
            base_construction = bien.prix_acquisition * bien.part_construction
            
            # Amortissement construction
            amort_construction_annuel = base_construction / bien.duree_amortissement_construction
            amort_construction_prorata = amort_construction_annuel * prorata
            
            # Amortissement frais de notaire
            amort_frais_notaire_annuel = bien.frais_notaire / bien.duree_amortissement_frais
            amort_frais_notaire_prorata = amort_frais_notaire_annuel * prorata
            
            # Amortissement frais d'agence
            amort_frais_agence_annuel = bien.frais_agence / bien.duree_amortissement_frais
            amort_frais_agence_prorata = amort_frais_agence_annuel * prorata
            
            # Totaux
            total_annuel = amort_construction_annuel + amort_frais_notaire_annuel + amort_frais_agence_annuel
            total_prorata = amort_construction_prorata + amort_frais_notaire_prorata + amort_frais_agence_prorata
            
            return Amortissement(
                construction_annuel=amort_construction_annuel.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                construction_prorata=amort_construction_prorata.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                frais_notaire_annuel=amort_frais_notaire_annuel.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                frais_notaire_prorata=amort_frais_notaire_prorata.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                frais_agence_annuel=amort_frais_agence_annuel.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                frais_agence_prorata=amort_frais_agence_prorata.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                total_annuel=total_annuel.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                total_prorata=total_prorata.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            )
            
        except Exception as e:
            logger.error(f"Erreur calcul amortissement: {e}")
            raise
    
    def calculer_total_depenses(self, depenses: Depenses) -> Decimal:
        """Calcule le total des dépenses déductibles"""
        return sum([
            depenses.frais_gestion,
            depenses.charges_copropriete,
            depenses.assurances,
            depenses.frais_menage_entretien,
            depenses.frais_plateformes,
            depenses.frais_comptabilite,
            depenses.abonnements,
            depenses.taxes_fonciere,
            depenses.taxes_habitation,
            depenses.taxe_sejour,
            depenses.cfe,
            depenses.charges_sociales,
            depenses.depenses_diverses,
            depenses.petits_travaux,
            depenses.petits_meubles
        ], Decimal('0'))
    
    def calculer_total_recettes(self, recettes: Recettes) -> Decimal:
        """Calcule le total des recettes"""
        return recettes.loyers_bruts + recettes.autres_recettes
    
    def calculer_total_interets(self, emprunt: Optional[Emprunt]) -> Decimal:
        """Calcule le total des intérêts d'emprunt déductibles"""
        if not emprunt:
            return Decimal('0')
        
        return sum([
            emprunt.interets_annuels,
            emprunt.assurance_emprunt,
            emprunt.frais_dossier,
            emprunt.frais_courtier
        ], Decimal('0'))
    
    def calculer_resultat_bien(
        self, 
        bien: BienImmobilier,
        recettes: Recettes,
        depenses: Depenses,
        emprunt: Optional[Emprunt] = None,
        annee: int = None
    ) -> Dict[str, Decimal]:
        """
        Calcule le résultat fiscal d'un bien LMNP
        """
        if annee is None:
            annee = self.annee_fiscale
            
        # Calculs des composants
        total_recettes = self.calculer_total_recettes(recettes)
        total_depenses = self.calculer_total_depenses(depenses)
        total_interets = self.calculer_total_interets(emprunt)
        amortissement = self.calculer_amortissement(bien, annee)
        
        # Utiliser le prorata pour la première année, sinon l'annuel
        amort_a_deduire = amortissement.total_prorata if annee == bien.date_entree_lmnp.year else amortissement.total_annuel
        
        # Résultat avant amortissement
        resultat_avant_amort = total_recettes - total_depenses - total_interets
        
        # Résultat après amortissement
        resultat_apres_amort = resultat_avant_amort - amort_a_deduire
        
        return {
            'recettes_totales': total_recettes.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            'depenses_totales': total_depenses.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            'interets_totaux': total_interets.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            'amortissements': amort_a_deduire.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            'resultat_avant_amortissement': resultat_avant_amort.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            'resultat_apres_amortissement': resultat_apres_amort.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        }
    
    def optimiser_regime_fiscal(self, recettes_totales: Decimal, charges_totales: Decimal) -> Dict[str, any]:
        """
        Compare micro-BIC vs régime réel et recommande le plus avantageux
        """
        # Calcul micro-BIC
        if recettes_totales <= self.SEUIL_MICRO_BIC:
            base_imposable_micro = recettes_totales * (Decimal('1') - self.ABATTEMENT_MICRO_BIC)
            micro_possible = True
        else:
            base_imposable_micro = recettes_totales  # Pas d'abattement si dépassement
            micro_possible = False
        
        # Calcul régime réel
        base_imposable_reel = recettes_totales - charges_totales
        
        # Recommandation
        if micro_possible and base_imposable_micro < base_imposable_reel:
            regime_recommande = "micro_bic"
            economie = base_imposable_reel - base_imposable_micro
        else:
            regime_recommande = "reel"
            economie = base_imposable_micro - base_imposable_reel if micro_possible else Decimal('0')
        
        return {
            'regime_recommande': regime_recommande,
            'micro_bic_possible': micro_possible,
            'base_imposable_micro': base_imposable_micro.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            'base_imposable_reel': base_imposable_reel.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            'economie_estimee': economie.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            'seuil_micro_bic': self.SEUIL_MICRO_BIC,
            'abattement_micro_bic': self.ABATTEMENT_MICRO_BIC
        }
    
    def valider_repartition_terrain_construction(self, part_terrain: Decimal, part_construction: Decimal) -> bool:
        """Valide que la répartition terrain/construction est cohérente"""
        total = part_terrain + part_construction
        return abs(total - Decimal('1')) < Decimal('0.01')  # Tolérance de 1%
    
    def suggerer_repartition_par_localisation(self, code_postal: str) -> Tuple[Decimal, Decimal]:
        """
        Suggère une répartition terrain/construction selon la localisation
        """
        # Règles simplifiées par zone géographique
        if code_postal.startswith(('75', '92', '93', '94')):  # Paris et petite couronne
            return Decimal('0.15'), Decimal('0.85')  # Terrain plus cher
        elif code_postal.startswith(('06', '83', '13')):  # Côte d'Azur, PACA
            return Decimal('0.25'), Decimal('0.75')  # Terrain valorisé
        elif code_postal.startswith(('01', '02', '03')):  # Zones rurales
            return Decimal('0.30'), Decimal('0.70')  # Terrain important
        else:
            return Decimal('0.20'), Decimal('0.80')  # Standard
    
    def calculer_cfe_estimee(self, recettes_annuelles: Decimal, commune: str = None) -> Decimal:
        """
        Estime la CFE (Cotisation Foncière des Entreprises)
        """
        # Base minimum CFE 2024
        base_minimum = Decimal('227')
        
        # Calcul simplifié basé sur les recettes
        if recettes_annuelles <= Decimal('5000'):
            return base_minimum
        elif recettes_annuelles <= Decimal('10000'):
            return base_minimum * Decimal('1.5')
        elif recettes_annuelles <= Decimal('32600'):
            return base_minimum * Decimal('2')
        else:
            # Calcul proportionnel pour les recettes plus importantes
            taux_estime = Decimal('0.002')  # 0.2% des recettes
            return max(base_minimum * Decimal('3'), recettes_annuelles * taux_estime)
    
    def generer_conseils_optimisation(self, resultats: Dict[str, Decimal]) -> List[str]:
        """
        Génère des conseils d'optimisation fiscale personnalisés
        """
        conseils = []
        
        recettes = resultats.get('recettes_totales', Decimal('0'))
        depenses = resultats.get('depenses_totales', Decimal('0'))
        resultat = resultats.get('resultat_apres_amortissement', Decimal('0'))
        
        # Conseils sur le régime fiscal
        if recettes <= self.SEUIL_MICRO_BIC:
            conseils.append("💡 Vous êtes éligible au régime micro-BIC avec 50% d'abattement automatique")
        
        # Conseils sur les charges
        ratio_charges = (depenses / recettes * 100) if recettes > 0 else Decimal('0')
        if ratio_charges < 20:
            conseils.append("⚠️ Vos charges semblent faibles. Vérifiez que vous déduisez toutes les dépenses possibles")
        elif ratio_charges > 60:
            conseils.append("📊 Vos charges sont importantes. Le régime réel pourrait être plus avantageux")
        
        # Conseils sur le résultat
        if resultat < 0:
            conseils.append("📉 Votre activité génère un déficit. Il sera reportable sur les bénéfices futurs")
        elif resultat > 0:
            conseils.append("📈 Votre activité est bénéficiaire. Pensez aux provisions pour charges futures")
        
        return conseils

# Instance globale de l'expert fiscal
expert_fiscal = ExpertiseFiscaleLMNP()

# Fonctions utilitaires pour l'utilisation dans l'application
def calculer_amortissement_bien(bien_data: Dict, annee: int = None) -> Dict:
    """Fonction utilitaire pour calculer les amortissements"""
    # Conversion des types pour éviter les erreurs float/Decimal
    bien_data_converted = {
        'id': bien_data['id'],
        'adresse': bien_data['adresse'],
        'date_entree_lmnp': bien_data['date_entree_lmnp'],
        'prix_acquisition': Decimal(str(bien_data['prix_acquisition'])),
        'frais_notaire': Decimal(str(bien_data['frais_notaire'])),
        'frais_agence': Decimal(str(bien_data['frais_agence']))
    }
    
    bien = BienImmobilier(**bien_data_converted)
    amortissement = expert_fiscal.calculer_amortissement(bien, annee or datetime.now().year)
    return {
        'construction_annuel': float(amortissement.construction_annuel),
        'construction_prorata': float(amortissement.construction_prorata),
        'frais_notaire_annuel': float(amortissement.frais_notaire_annuel),
        'frais_notaire_prorata': float(amortissement.frais_notaire_prorata),
        'frais_agence_annuel': float(amortissement.frais_agence_annuel),
        'frais_agence_prorata': float(amortissement.frais_agence_prorata),
        'total_annuel': float(amortissement.total_annuel),
        'total_prorata': float(amortissement.total_prorata)
    }

def calculer_resultat_fiscal(bien_data: Dict, recettes_data: Dict, depenses_data: Dict, emprunt_data: Dict = None) -> Dict:
    """Fonction utilitaire pour calculer le résultat fiscal complet"""
    bien = BienImmobilier(**bien_data)
    recettes = Recettes(**recettes_data)
    depenses = Depenses(**depenses_data)
    emprunt = Emprunt(**emprunt_data) if emprunt_data else None
    
    resultats = expert_fiscal.calculer_resultat_bien(bien, recettes, depenses, emprunt)
    
    # Conversion en float pour JSON
    return {k: float(v) for k, v in resultats.items()}

def optimiser_regime(recettes_totales: float, charges_totales: float) -> Dict:
    """Fonction utilitaire pour l'optimisation du régime fiscal"""
    optimisation = expert_fiscal.optimiser_regime_fiscal(Decimal(str(recettes_totales)), Decimal(str(charges_totales)))
    
    # Conversion en types JSON-compatibles
    return {
        'regime_recommande': optimisation['regime_recommande'],
        'micro_bic_possible': optimisation['micro_bic_possible'],
        'base_imposable_micro': float(optimisation['base_imposable_micro']),
        'base_imposable_reel': float(optimisation['base_imposable_reel']),
        'economie_estimee': float(optimisation['economie_estimee']),
        'seuil_micro_bic': float(optimisation['seuil_micro_bic']),
        'abattement_micro_bic': float(optimisation['abattement_micro_bic'])
    }

