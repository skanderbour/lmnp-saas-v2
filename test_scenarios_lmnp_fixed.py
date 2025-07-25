#!/usr/bin/env python3
"""
Scénarios de tests utilisateur pour l'application LMNP SAAS
Simulation de cas d'usage réels avec différents profils d'utilisateurs
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Any

class LMNPUserScenarios:
    def __init__(self):
        self.base_url = "http://localhost:5000"
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        
    def scenario_marie_debutante(self):
        """Scénario 1: Marie, 28 ans, première expérience LMNP"""
        print("🏠 SCÉNARIO 1: Marie - Débutante LMNP")
        print("-" * 40)
        
        timestamp = int(time.time())
        user_data = {
            "nom": "Marie Dubois",
            "email": f"marie.dubois.{timestamp}@email.com",
            "telephone": "0123456789",
            "profile": "debutant"
        }
        
        user_response = self.session.post(f"{self.base_url}/api/lmnp/users", json=user_data)
        if user_response.status_code != 201:
            print(f"❌ Échec création utilisateur: {user_response.text}")
            return False
        
        user_id = user_response.json().get("user", {}).get("id")
        print(f"✅ Utilisateur créé: ID {user_id}")
        
        # Création bien immobilier
        bien_data = {
            "nom": "Studio Étudiant Lyon",
            "type_location": "longue_duree",
            "adresse": "15 Rue de la République",
            "code_postal": "69002",
            "ville": "Lyon",
            "surface": 25,
            "nb_pieces": 1,
            "date_acquisition": "2024-01-15",
            "prix_acquisition": 120000,
            "frais_notaire": 8000,
            "valeur_mobilier": 15000,
            "loyer_mensuel": 650,
            "user_id": user_id
        }
        
        bien_response = self.session.post(f"{self.base_url}/api/lmnp/biens", json=bien_data)
        if bien_response.status_code != 201:
            print(f"❌ Échec création bien: {bien_response.text}")
            return False
        
        print("✅ Bien immobilier créé")
        print("✅ Scénario Marie terminé avec succès")
        return True
        
    def scenario_jean_experimente(self):
        """Scénario 2: Jean, 45 ans, investisseur expérimenté"""
        print("🏢 SCÉNARIO 2: Jean - Expérimenté LMNP")
        print("-" * 40)
        
        timestamp = int(time.time()) + 1
        user_data = {
            "nom": "Jean Martin",
            "email": f"jean.martin.{timestamp}@email.com",
            "telephone": "0234567890",
            "profile": "experimente"
        }
        
        user_response = self.session.post(f"{self.base_url}/api/lmnp/users", json=user_data)
        if user_response.status_code != 201:
            print(f"❌ Échec création utilisateur: {user_response.text}")
            return False
        
        user_id = user_response.json().get("user", {}).get("id")
        print(f"✅ Utilisateur créé: ID {user_id}")
        
        # Création de plusieurs biens
        biens = [
            {
                "nom": "Appartement T3 Paris",
                "type_location": "tourisme_classe",
                "adresse": "25 Avenue des Champs-Élysées",
                "code_postal": "75008",
                "ville": "Paris",
                "surface": 75,
                "nb_pieces": 3,
                "date_acquisition": "2023-06-01",
                "prix_acquisition": 450000,
                "frais_notaire": 35000,
                "valeur_mobilier": 25000,
                "loyer_mensuel": 2800,
                "user_id": user_id
            },
            {
                "nom": "Villa Côte d'Azur",
                "type_location": "tourisme_non_classe",
                "adresse": "12 Promenade des Anglais",
                "code_postal": "06000",
                "ville": "Nice",
                "surface": 120,
                "nb_pieces": 5,
                "date_acquisition": "2023-03-15",
                "prix_acquisition": 680000,
                "frais_notaire": 52000,
                "valeur_mobilier": 45000,
                "loyer_mensuel": 4200,
                "user_id": user_id
            }
        ]
        
        for i, bien_data in enumerate(biens):
            bien_response = self.session.post(f"{self.base_url}/api/lmnp/biens", json=bien_data)
            if bien_response.status_code != 201:
                print(f"❌ Échec création bien {i+1}: {bien_response.text}")
                return False
            print(f"✅ Bien {i+1} créé: {bien_data['nom']}")
        
        print("✅ Scénario Jean terminé avec succès")
        return True
        
    def scenario_sophie_professionnelle(self):
        """Scénario 3: Sophie, 35 ans, professionnelle de l'immobilier"""
        print("🏛️ SCÉNARIO 3: Sophie - Professionnelle Immobilier")
        print("-" * 40)
        
        timestamp = int(time.time()) + 2
        user_data = {
            "nom": "Sophie Leroy",
            "email": f"sophie.leroy.{timestamp}@email.com",
            "telephone": "0345678901",
            "profile": "professionnel"
        }
        
        user_response = self.session.post(f"{self.base_url}/api/lmnp/users", json=user_data)
        if user_response.status_code != 201:
            print(f"❌ Échec création utilisateur: {user_response.text}")
            return False
        
        user_id = user_response.json().get("user", {}).get("id")
        print(f"✅ Utilisateur créé: ID {user_id}")
        
        # Test des agents IA
        agents_response = self.session.get(f"{self.base_url}/api/agents/list")
        if agents_response.status_code == 200:
            agents = agents_response.json()
            print(f"✅ {len(agents)} agents IA disponibles")
        
        # Test analyse transaction
        transaction_data = {
            "libelle": "Travaux rénovation salle de bain",
            "montant": 3500.00,
            "date": "2024-02-20"
        }
        
        analysis_response = self.session.post(f"{self.base_url}/api/agents/analyze-transaction", json=transaction_data)
        if analysis_response.status_code == 200:
            analysis = analysis_response.json()
            print(f"✅ Analyse IA: {analysis.get('category', 'N/A')}")
        
        print("✅ Scénario Sophie terminé avec succès")
        return True
        
    def scenario_cas_limites(self):
        """Scénario 4: Tests des cas limites et edge cases"""
        print("⚠️ SCÉNARIO 4: Cas Limites et Edge Cases")
        print("-" * 40)
        
        # Test 1: Valeurs extrêmes
        timestamp = int(time.time()) + 3
        user_data = {
            "nom": "Test Limites",
            "email": f"test.limites.{timestamp}@email.com",
            "telephone": "0456789012",
            "profile": "test"
        }
        
        user_response = self.session.post(f"{self.base_url}/api/lmnp/users", json=user_data)
        if user_response.status_code != 201:
            print(f"❌ Échec création utilisateur: {user_response.text}")
            return False
        
        user_id = user_response.json().get("user", {}).get("id")
        print(f"✅ Utilisateur test créé: ID {user_id}")
        
        # Test bien avec valeurs limites
        bien_limite = {
            "nom": "Bien Test Limites",
            "type_location": "chambre_hotes",
            "adresse": "1 Rue du Test",
            "code_postal": "01000",
            "ville": "Test",
            "surface": 1000,  # Grande surface
            "nb_pieces": 20,  # Beaucoup de pièces
            "date_acquisition": "2024-12-31",
            "prix_acquisition": 1000000,  # Prix élevé
            "frais_notaire": 100000,
            "valeur_mobilier": 200000,
            "loyer_mensuel": 8000,
            "user_id": user_id
        }
        
        bien_response = self.session.post(f"{self.base_url}/api/lmnp/biens", json=bien_limite)
        if bien_response.status_code == 201:
            print("✅ Test valeurs limites: PASS")
        else:
            print(f"❌ Test valeurs limites: {bien_response.text}")
        
        print("✅ Scénario cas limites terminé")
        return True
        
    def run_all_scenarios(self):
        """Exécuter tous les scénarios"""
        print("🎭 SCÉNARIOS UTILISATEUR LMNP SAAS")
        print("=" * 50)
        
        scenarios = [
            ("Marie - Débutante", self.scenario_marie_debutante),
            ("Jean - Expérimenté", self.scenario_jean_experimente),
            ("Sophie - Professionnelle", self.scenario_sophie_professionnelle),
            ("Cas Limites", self.scenario_cas_limites)
        ]
        
        results = []
        
        for name, scenario_func in scenarios:
            try:
                success = scenario_func()
                results.append((name, success))
                print()
            except Exception as e:
                print(f"❌ Erreur dans le scénario {name}: {str(e)}")
                results.append((name, False))
                print()
        
        # Résumé
        print("=" * 50)
        print("📊 RÉSUMÉ DES SCÉNARIOS")
        print("=" * 50)
        
        total = len(results)
        success_count = sum(1 for _, success in results if success)
        
        print(f"Scénarios exécutés: {total}")
        print(f"✅ Réussis: {success_count}")
        print(f"❌ Échoués: {total - success_count}")
        
        for name, success in results:
            status = "✅" if success else "❌"
            print(f"{status} {name}")

if __name__ == "__main__":
    scenarios = LMNPUserScenarios()
    scenarios.run_all_scenarios()

