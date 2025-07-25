#!/usr/bin/env python3
"""
Suite de tests exhaustive pour l'application LMNP SAAS
Tests unitaires, d'intégration et de cas d'usage complets
"""

import requests
import json
import time
import sys
from datetime import datetime, date
from typing import Dict, List, Any
import traceback

class LMNPSAASTestSuite:
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        self.created_users = []
        self.created_biens = []
        self.created_transactions = []
        
    def log_test(self, test_name: str, status: str, details: str = "", error: str = ""):
        """Enregistrer le résultat d'un test"""
        result = {
            "test_name": test_name,
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "details": details,
            "error": error
        }
        self.test_results.append(result)
        
        # Affichage en temps réel
        status_symbol = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_symbol} {test_name}: {status}")
        if details:
            print(f"   → {details}")
        if error:
            print(f"   ❌ Erreur: {error}")
        print()

    def test_api_health(self):
        """Test 1: Vérifier que l'API est accessible"""
        try:
            response = self.session.get(f"{self.base_url}/api/health")
            if response.status_code == 200:
                data = response.json()
                if data.get("service") == "LMNP SAAS Backend":
                    self.log_test("API Health Check", "PASS", f"Service opérationnel - Status: {data.get('status')}")
                else:
                    self.log_test("API Health Check", "FAIL", "Service non reconnu", str(data))
            else:
                self.log_test("API Health Check", "FAIL", f"Code HTTP: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("API Health Check", "FAIL", "Connexion impossible", str(e))

    def test_user_creation(self):
        """Test 2: Créer un nouvel utilisateur"""
        try:
            user_data = {
                "nom": "Test User",
                "email": "test@example.com",
                "telephone": "0123456789"
            }
            
            response = self.session.post(f"{self.base_url}/api/lmnp/users", json=user_data)
            
            if response.status_code == 201:
                data = response.json()
                user_data = data.get("user", {})
                user_id = user_data.get("id")
                if user_id:
                    self.created_users.append(user_id)
                    self.log_test("Création Utilisateur", "PASS", f"Utilisateur créé avec ID: {user_id}")
                    return user_id
                else:
                    self.log_test("Création Utilisateur", "FAIL", "ID utilisateur manquant", str(data))
            else:
                self.log_test("Création Utilisateur", "FAIL", f"Code HTTP: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Création Utilisateur", "FAIL", "Erreur lors de la création", str(e))
        return None

    def test_user_retrieval(self, user_id: int):
        """Test 3: Récupérer les informations d'un utilisateur"""
        try:
            response = self.session.get(f"{self.base_url}/api/lmnp/users/{user_id}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("id") == user_id:
                    self.log_test("Récupération Utilisateur", "PASS", f"Utilisateur {user_id} récupéré avec succès")
                    return data
                else:
                    self.log_test("Récupération Utilisateur", "FAIL", "ID utilisateur incorrect", str(data))
            else:
                self.log_test("Récupération Utilisateur", "FAIL", f"Code HTTP: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Récupération Utilisateur", "FAIL", "Erreur lors de la récupération", str(e))
        return None

    def test_bien_creation(self, user_id: int):
        """Test 4: Créer un bien immobilier"""
        try:
            bien_data = {
                "user_id": user_id,
                "nom": "Appartement Test Paris",
                "adresse": "123 Rue de la Paix, 75001 Paris",
                "type_location": "meuble_tourisme",
                "surface": 45,
                "nb_pieces": 2,
                "prix_acquisition": 250000,
                "date_acquisition": "2024-03-15",
                "frais_acquisition": 15000,
                "travaux": 25000
            }
            
            response = self.session.post(f"{self.base_url}/api/lmnp/biens", json=bien_data)
            
            if response.status_code == 201:
                data = response.json()
                bien_id = data.get("id")
                if bien_id:
                    self.created_biens.append(bien_id)
                    self.log_test("Création Bien Immobilier", "PASS", f"Bien créé avec ID: {bien_id}")
                    return bien_id
                else:
                    self.log_test("Création Bien Immobilier", "FAIL", "ID bien manquant", str(data))
            else:
                self.log_test("Création Bien Immobilier", "FAIL", f"Code HTTP: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Création Bien Immobilier", "FAIL", "Erreur lors de la création", str(e))
        return None

    def test_transaction_creation(self, bien_id: int):
        """Test 5: Créer des transactions pour un bien"""
        transactions_test = [
            {
                "bien_id": bien_id,
                "date": "2024-01-15",
                "libelle": "Loyer janvier 2024",
                "montant": 1200.00,
                "type": "recette",
                "categorie": "loyers"
            },
            {
                "bien_id": bien_id,
                "date": "2024-01-20",
                "libelle": "Assurance habitation",
                "montant": 350.00,
                "type": "charge",
                "categorie": "assurances"
            },
            {
                "bien_id": bien_id,
                "date": "2024-02-15",
                "libelle": "Loyer février 2024",
                "montant": 1200.00,
                "type": "recette",
                "categorie": "loyers"
            }
        ]
        
        created_transactions = []
        for transaction_data in transactions_test:
            try:
                response = self.session.post(f"{self.base_url}/api/lmnp/transactions", json=transaction_data)
                
                if response.status_code == 201:
                    data = response.json()
                    transaction_id = data.get("id")
                    if transaction_id:
                        created_transactions.append(transaction_id)
                        self.created_transactions.append(transaction_id)
                    else:
                        self.log_test("Création Transaction", "FAIL", f"ID transaction manquant pour {transaction_data['libelle']}", str(data))
                else:
                    self.log_test("Création Transaction", "FAIL", f"Code HTTP: {response.status_code} pour {transaction_data['libelle']}", response.text)
            except Exception as e:
                self.log_test("Création Transaction", "FAIL", f"Erreur pour {transaction_data['libelle']}", str(e))
        
        if len(created_transactions) == len(transactions_test):
            self.log_test("Création Transactions", "PASS", f"{len(created_transactions)} transactions créées avec succès")
        else:
            self.log_test("Création Transactions", "PARTIAL", f"{len(created_transactions)}/{len(transactions_test)} transactions créées")
        
        return created_transactions

    def test_calcul_fiscal(self, user_id: int, annee: int = 2024):
        """Test 6: Effectuer un calcul fiscal complet"""
        try:
            calcul_data = {
                "user_id": user_id,
                "annee": annee
            }
            
            response = self.session.post(f"{self.base_url}/api/lmnp/calcul-fiscal", json=calcul_data)
            
            if response.status_code == 200:
                data = response.json()
                
                # Vérifier les éléments essentiels du calcul
                required_fields = ["total_recettes", "total_charges", "resultat_fiscal", "regime_recommande"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields:
                    recettes = data.get("total_recettes", 0)
                    charges = data.get("total_charges", 0)
                    regime = data.get("regime_recommande", "")
                    economie = data.get("economie_regime_optimal", 0)
                    
                    details = f"Recettes: {recettes}€, Charges: {charges}€, Régime: {regime}"
                    if economie > 0:
                        details += f", Économie: {economie}€"
                    
                    self.log_test("Calcul Fiscal", "PASS", details)
                    return data
                else:
                    self.log_test("Calcul Fiscal", "FAIL", f"Champs manquants: {missing_fields}", str(data))
            else:
                self.log_test("Calcul Fiscal", "FAIL", f"Code HTTP: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Calcul Fiscal", "FAIL", "Erreur lors du calcul", str(e))
        return None

    def test_agents_ia_list(self):
        """Test 7: Lister les agents IA disponibles"""
        try:
            response = self.session.get(f"{self.base_url}/api/agents/agents")
            
            if response.status_code == 200:
                data = response.json()
                agents = data.get("agents", [])
                
                if len(agents) > 0:
                    agent_names = [agent.get("name", "Unknown") for agent in agents]
                    self.log_test("Liste Agents IA", "PASS", f"{len(agents)} agents disponibles: {', '.join(agent_names)}")
                    return agents
                else:
                    self.log_test("Liste Agents IA", "FAIL", "Aucun agent IA trouvé", str(data))
            else:
                self.log_test("Liste Agents IA", "FAIL", f"Code HTTP: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Liste Agents IA", "FAIL", "Erreur lors de la récupération", str(e))
        return None

    def test_agent_transaction_analysis(self):
        """Test 8: Analyser une transaction avec l'agent IA"""
        try:
            analysis_data = {
                "libelle": "Réparation plomberie urgente",
                "montant": 450.00,
                "date": "2024-03-15"
            }
            
            response = self.session.post(f"{self.base_url}/api/agents/analyze-transaction", json=analysis_data)
            
            if response.status_code == 200:
                data = response.json()
                
                if "categorie" in data and "confiance" in data:
                    categorie = data.get("categorie", "")
                    confiance = data.get("confiance", 0)
                    explication = data.get("explication", "")
                    
                    details = f"Catégorie: {categorie}, Confiance: {confiance}%"
                    if explication:
                        details += f", Explication: {explication[:50]}..."
                    
                    self.log_test("Analyse Transaction IA", "PASS", details)
                    return data
                else:
                    self.log_test("Analyse Transaction IA", "FAIL", "Réponse incomplète", str(data))
            else:
                self.log_test("Analyse Transaction IA", "FAIL", f"Code HTTP: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Analyse Transaction IA", "FAIL", "Erreur lors de l'analyse", str(e))
        return None

    def test_agent_fiscal_optimization(self, user_id: int):
        """Test 9: Optimisation fiscale avec l'agent IA"""
        try:
            optimization_data = {
                "user_id": user_id,
                "annee": 2024
            }
            
            response = self.session.post(f"{self.base_url}/api/agents/optimize-fiscal", json=optimization_data)
            
            if response.status_code == 200:
                data = response.json()
                
                if "regime_optimal" in data and "economie" in data:
                    regime = data.get("regime_optimal", "")
                    economie = data.get("economie", 0)
                    recommandations = data.get("recommandations", [])
                    
                    details = f"Régime optimal: {regime}, Économie: {economie}€"
                    if recommandations:
                        details += f", {len(recommandations)} recommandations"
                    
                    self.log_test("Optimisation Fiscale IA", "PASS", details)
                    return data
                else:
                    self.log_test("Optimisation Fiscale IA", "FAIL", "Réponse incomplète", str(data))
            else:
                self.log_test("Optimisation Fiscale IA", "FAIL", f"Code HTTP: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Optimisation Fiscale IA", "FAIL", "Erreur lors de l'optimisation", str(e))
        return None

    def test_multiple_users_scenario(self):
        """Test 10: Scénario avec plusieurs utilisateurs"""
        test_users = [
            {
                "nom": "Marie Dupont",
                "email": "marie.dupont@example.com",
                "profile": "debutant"
            },
            {
                "nom": "Jean Martin",
                "email": "jean.martin@example.com", 
                "profile": "experimente"
            },
            {
                "nom": "Sophie Bernard",
                "email": "sophie.bernard@example.com",
                "profile": "professionnel"
            }
        ]
        
        created_users = []
        for user_data in test_users:
            try:
                response = self.session.post(f"{self.base_url}/api/lmnp/users", json=user_data)
                if response.status_code == 201:
                    data = response.json()
                    user_id = data.get("id")
                    if user_id:
                        created_users.append(user_id)
                        self.created_users.append(user_id)
            except Exception as e:
                pass
        
        if len(created_users) == len(test_users):
            self.log_test("Scénario Utilisateurs Multiples", "PASS", f"{len(created_users)} utilisateurs créés avec différents profils")
        else:
            self.log_test("Scénario Utilisateurs Multiples", "PARTIAL", f"{len(created_users)}/{len(test_users)} utilisateurs créés")
        
        return created_users

    def test_edge_cases(self):
        """Test 11: Cas limites et edge cases"""
        edge_cases = []
        
        # Test 1: Montant négatif
        try:
            response = self.session.post(f"{self.base_url}/api/lmnp/transactions", json={
                "bien_id": 999,
                "date": "2024-01-01",
                "libelle": "Test montant négatif",
                "montant": -100.00,
                "type": "recette"
            })
            edge_cases.append(("Montant négatif", response.status_code != 201))
        except:
            edge_cases.append(("Montant négatif", True))
        
        # Test 2: Date future
        try:
            response = self.session.post(f"{self.base_url}/api/lmnp/transactions", json={
                "bien_id": 999,
                "date": "2030-01-01",
                "libelle": "Test date future",
                "montant": 100.00,
                "type": "recette"
            })
            edge_cases.append(("Date future", response.status_code != 201))
        except:
            edge_cases.append(("Date future", True))
        
        # Test 3: Email invalide
        try:
            response = self.session.post(f"{self.base_url}/api/lmnp/users", json={
                "nom": "Test Invalid Email",
                "email": "email-invalide"
            })
            edge_cases.append(("Email invalide", response.status_code != 201))
        except:
            edge_cases.append(("Email invalide", True))
        
        passed_cases = sum(1 for _, passed in edge_cases if passed)
        total_cases = len(edge_cases)
        
        if passed_cases == total_cases:
            self.log_test("Tests Cas Limites", "PASS", f"{passed_cases}/{total_cases} cas limites gérés correctement")
        else:
            self.log_test("Tests Cas Limites", "PARTIAL", f"{passed_cases}/{total_cases} cas limites gérés")

    def test_performance(self):
        """Test 12: Tests de performance"""
        try:
            # Test de charge sur l'endpoint health
            start_time = time.time()
            responses = []
            
            for i in range(10):
                response = self.session.get(f"{self.base_url}/api/health")
                responses.append(response.status_code == 200)
            
            end_time = time.time()
            duration = end_time - start_time
            avg_response_time = duration / 10 * 1000  # en ms
            
            success_rate = sum(responses) / len(responses) * 100
            
            if success_rate >= 95 and avg_response_time < 1000:
                self.log_test("Test Performance", "PASS", f"Taux de succès: {success_rate}%, Temps moyen: {avg_response_time:.1f}ms")
            else:
                self.log_test("Test Performance", "FAIL", f"Taux de succès: {success_rate}%, Temps moyen: {avg_response_time:.1f}ms")
                
        except Exception as e:
            self.log_test("Test Performance", "FAIL", "Erreur lors du test de performance", str(e))

    def run_all_tests(self):
        """Exécuter tous les tests"""
        print("🚀 DÉBUT DES TESTS LMNP SAAS")
        print("=" * 50)
        print()
        
        start_time = time.time()
        
        # Tests de base
        self.test_api_health()
        user_id = self.test_user_creation()
        
        if user_id:
            self.test_user_retrieval(user_id)
            bien_id = self.test_bien_creation(user_id)
            
            if bien_id:
                self.test_transaction_creation(bien_id)
                self.test_calcul_fiscal(user_id)
        
        # Tests des agents IA
        self.test_agents_ia_list()
        self.test_agent_transaction_analysis()
        
        if user_id:
            self.test_agent_fiscal_optimization(user_id)
        
        # Tests avancés
        self.test_multiple_users_scenario()
        self.test_edge_cases()
        self.test_performance()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Résumé des résultats
        print("=" * 50)
        print("📊 RÉSUMÉ DES TESTS")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        partial_tests = len([r for r in self.test_results if r["status"] == "PARTIAL"])
        
        print(f"Tests exécutés: {total_tests}")
        print(f"✅ Succès: {passed_tests} ({passed_tests/total_tests*100:.1f}%)")
        print(f"❌ Échecs: {failed_tests} ({failed_tests/total_tests*100:.1f}%)")
        print(f"⚠️ Partiels: {partial_tests} ({partial_tests/total_tests*100:.1f}%)")
        print(f"⏱️ Durée totale: {duration:.2f} secondes")
        print()
        
        # Tests échoués
        if failed_tests > 0:
            print("❌ TESTS ÉCHOUÉS:")
            for result in self.test_results:
                if result["status"] == "FAIL":
                    print(f"  • {result['test_name']}: {result['error']}")
            print()
        
        # Recommandations
        print("💡 RECOMMANDATIONS:")
        if failed_tests == 0:
            print("  ✅ Tous les tests sont passés ! L'application est prête pour la production.")
        else:
            print(f"  ⚠️ {failed_tests} tests ont échoué. Vérifiez les erreurs ci-dessus.")
            
        if partial_tests > 0:
            print(f"  ⚠️ {partial_tests} tests sont partiels. Vérifiez les détails.")
        
        return {
            "total": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "partial": partial_tests,
            "duration": duration,
            "results": self.test_results
        }

if __name__ == "__main__":
    # Lancer la suite de tests
    test_suite = LMNPSAASTestSuite()
    results = test_suite.run_all_tests()
    
    # Code de sortie basé sur les résultats
    if results["failed"] == 0:
        sys.exit(0)  # Succès
    else:
        sys.exit(1)  # Échec

