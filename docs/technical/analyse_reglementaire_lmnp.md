# Analyse Réglementaire LMNP - Sources Officielles

## 1. BOI-BIC-CHAMP-40-20 - Régime fiscal de la location meublée

**Source :** https://bofip.impots.gouv.fr/bofip/3610-PGP.html/identifiant=BOI-BIC-CHAMP-40-20-20240214
**Date de publication :** 14/02/2024
**Identifiant juridique :** BOI-BIC-CHAMP-40-20

### I. Principes généraux

#### A. Caractéristiques de la location meublée

**Points clés :**
- Les profits provenant de la location en meublé (habituelle ou occasionnelle) relèvent des BIC
- Applicable quel que soit le statut du bailleur (propriétaire ou locataire principal)
- Le fait que le bailleur n'intervienne pas dans l'entretien des meubles n'empêche pas l'imposition BIC

**Sociétés civiles :**
- Une société civile louant des locaux garnis est considérée comme exerçant une profession commerciale
- Exception : activité commerciale accessoire < 10% des recettes totales HT (reste à l'IR)
- Pour les sociétés civiles agricoles : seuils de l'article 75 du CGI

#### B. Éligibilité au régime des micro-entreprises

**Modifications 2024 (Article 45 de la loi de finances 2024) :**
- Pour les meublés de tourisme non classés : seuil abaissé à 15 000 € avec abattement de 30%
- Application rétroactive aux revenus 2023 (mais tolérance administrative possible)

**Seuils selon le type de location :**

1. **Meublés de tourisme et chambres d'hôtes** (art. 1407 du CGI, 2° et 3°) :
   - Seuil : celui du 1° de l'article 50-0 du CGI
   - Abattement forfaitaire : 71%
   - Condition : classement obligatoire pour les meublés de tourisme

2. **Autres locations meublées** :
   - Seuil : celui du 2° de l'article 50-0 du CGI  
   - Abattement forfaitaire : 50%

**Définitions importantes :**
- **Meublés de tourisme :** nécessitent un classement (art. L. 324-1 du code du tourisme)
- **Chambres d'hôtes :** chambres meublées chez l'habitant pour touristes (art. L. 324-3 du code du tourisme)

#### C. Détermination du résultat imposable (régime réel)

**Obligations comptables :**
- Comptabilité complète
- Compte de résultat et bilan
- Inscription des biens loués à l'actif

**Règles d'amortissement (art. 39 C du CGI) :**
- Limitation : amortissement ≤ loyer acquis - autres charges
- Application aux immeubles et meubles
- Référence : BOI-BIC-AMT-20-40-10

**Immobilisations non dépréciables :**
- Terrains et autres biens non dépréciables (art. 38 sexies annexe III CGI)
- Ne peuvent pas être amortis

### Points d'attention pour le développement de l'outil :

1. **Gestion des seuils différenciés** selon le type de location
2. **Calcul automatique des amortissements** avec limitation légale
3. **Distinction meublé classé/non classé** pour l'application des bons taux
4. **Gestion de la rétroactivité 2023** pour les nouvelles règles
5. **Obligations comptables** selon le régime choisi




## II. Exonérations (Article 35 bis du CGI)

### A. Location en meublé

**Conditions d'exonération :**

1. **Première condition - Nature des locaux :**
   - Pièces louées = partie de la résidence principale du bailleur
   - Contrat de travail conclu en application de l'article L. 1242-2 du code du travail
   - Prix de location fixé dans des limites raisonnables

2. **Deuxième condition - Seuils :**
   - Location habituelle à des personnes n'y élisant pas domicile (chambres d'hôtes)
   - Seuil : ne pas excéder 760 € par an (CGI, art. 35 bis, I)

**Application temporaire (loi de finances 2024) :**
- Dispositif d'exonération de l'article 35 bis du CGI
- Applicable aux locations/sous-locations jusqu'au 31 décembre 2026
- Concerne l'article 38 de la loi n° 2023-1322 du 29 décembre 2023

**Cumul d'exonérations :**
- Les deux exonérations peuvent se cumuler pour un local loué à des lycéens ou étudiants
- Période : année scolaire + vacanciers durant la période estivale
- Référence : RM Authié n° 20969, JO Sénat du 21 février 1985

**Attention :** L'exonération des chambres d'hôtes ne peut pas se cumuler avec les dispositions de l'article 50-0 du CGI (micro-BIC).

### Points d'attention pour l'outil :

1. **Vérification des conditions d'exonération** avant calcul
2. **Gestion des seuils** (760 € pour chambres d'hôtes)
3. **Contrôle du cumul** des exonérations
4. **Application temporaire** jusqu'en 2026
5. **Incompatibilité** exonération chambres d'hôtes + micro-BIC


## III. Plafonds Micro-BIC LMNP 2023-2025

### Évolution des Seuils (Loi de Finances 2024)

**Changements majeurs introduits par l'article 45 de la loi n° 2023-1322 du 29 décembre 2023 :**

#### 1. **Meublés de Tourisme Non Classés**
- **Avant 2024 :** 77 700 € (abattement 50%)
- **À partir de 2024 :** 15 000 € (abattement 30%)
- **Application rétroactive :** Revenus 2023 (avec tolérance administrative)

#### 2. **Meublés de Tourisme Classés + Chambres d'Hôtes**
- **Seuil maintenu :** 77 700 € (anciennement 188 700 €)
- **Abattement :** 71% (inchangé)
- **Condition :** Classement obligatoire délivré par organisme agréé

#### 3. **Locations Meublées Longue Durée**
- **Seuil :** 77 700 € (inchangé)
- **Abattement :** 50% (inchangé)

### Seuils LMNP vs LMP (Passage en Professionnel)

**Conditions cumulatives pour rester en LMNP :**
1. **Recettes annuelles ≤ 23 000 €** OU
2. **Recettes ≤ 50% des revenus du foyer fiscal**

**Au-delà :** Basculement automatique en LMP (Loueur en Meublé Professionnel)

### Tolérance de Dépassement

**Règle générale :**
- Dépassement possible **1 ou 2 années consécutives**
- Maintien du micro-BIC une année supplémentaire
- Au-delà : basculement automatique en régime réel

### Tableau Récapitulatif 2025

| Type de Location | Seuil Micro-BIC | Abattement | Régime au-delà |
|------------------|-----------------|------------|----------------|
| **Meublé longue durée** | 77 700 € | 50% | Régime réel BIC |
| **Meublé tourisme classé** | 77 700 € | 71% | Régime réel BIC |
| **Meublé tourisme non classé** | 15 000 € | 30% | Régime réel BIC |
| **Chambres d'hôtes** | 77 700 € | 71% | Régime réel BIC |

### Points d'Attention pour l'Outil

#### **Gestion des Transitions :**
1. **Détection automatique** du type de location (classé/non classé)
2. **Calcul des seuils** selon la nature du bien
3. **Alerte de dépassement** avec simulation régime réel
4. **Gestion de la tolérance** sur 1-2 ans

#### **Vérifications Obligatoires :**
1. **Classement touristique** (certificat requis)
2. **Nature de l'activité** (occasionnelle vs habituelle)
3. **Cumul des revenus** pour seuil LMP
4. **Prorata temporis** en cas de début d'activité

#### **Optimisation Fiscale :**
1. **Comparaison micro-BIC vs réel** automatique
2. **Simulation impact** changement de régime
3. **Conseil personnalisé** selon situation
4. **Anticipation** des seuils futurs

### Cas Particuliers

#### **Indivision :**
- Seuils appliqués **par indivisaire**
- Déclaration séparée obligatoire
- Quote-part proportionnelle

#### **Activités Mixtes :**
- Cumul possible avec autres BIC
- Seuils globaux à respecter
- Ventilation par activité

#### **Première Année :**
- **Prorata temporis** selon date de début
- Seuils ajustés à la durée d'exploitation
- Déclaration obligatoire même si < seuil

