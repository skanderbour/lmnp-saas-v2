# Guide de Contribution

Merci de votre intérêt pour contribuer à LMNP SAAS ! Ce guide vous explique comment participer au développement du projet.

## 🤝 Comment contribuer

### Types de contributions

- 🐛 **Correction de bugs**
- ✨ **Nouvelles fonctionnalités**
- 📚 **Amélioration de la documentation**
- 🧪 **Ajout de tests**
- 🎨 **Améliorations UI/UX**
- 🔧 **Optimisations de performance**

### Processus de contribution

1. **Fork** le projet
2. **Créer** une branche pour votre fonctionnalité
3. **Développer** et tester vos modifications
4. **Commiter** avec des messages clairs
5. **Pousser** vers votre fork
6. **Créer** une Pull Request

## 🚀 Configuration de développement

### 1. Fork et clone

```bash
# Fork le projet sur GitHub, puis :
git clone https://github.com/votre-username/lmnp-saas.git
cd lmnp-saas
git remote add upstream https://github.com/original-username/lmnp-saas.git
```

### 2. Installation

Suivez le [guide d'installation](INSTALL.md) pour configurer votre environnement de développement.

### 3. Créer une branche

```bash
git checkout -b feature/ma-nouvelle-fonctionnalite
# ou
git checkout -b fix/correction-bug-xyz
```

## 📝 Standards de code

### Backend (Python)

- **Style** : PEP 8
- **Formatage** : Black
- **Linting** : Flake8
- **Type hints** : Recommandé

```bash
# Formatage automatique
black src/

# Vérification du style
flake8 src/
```

### Frontend (JavaScript/React)

- **Style** : ESLint + Prettier
- **Conventions** : Airbnb style guide
- **Composants** : Functional components avec hooks

```bash
# Formatage automatique
npm run format

# Vérification du style
npm run lint
```

### Conventions de nommage

- **Variables** : camelCase (JS) / snake_case (Python)
- **Fonctions** : camelCase (JS) / snake_case (Python)
- **Classes** : PascalCase
- **Constantes** : UPPER_SNAKE_CASE
- **Fichiers** : kebab-case ou snake_case

## 🧪 Tests

### Tests obligatoires

Toute nouvelle fonctionnalité doit inclure des tests :

```bash
# Tests backend
cd backend
python -m pytest tests/ -v --cov=src

# Tests frontend
cd frontend
npm run test
```

### Types de tests

- **Unitaires** : Fonctions individuelles
- **Intégration** : API endpoints
- **E2E** : Parcours utilisateur complets

### Couverture de code

Objectif : **80%+ de couverture**

## 📋 Messages de commit

Utilisez le format [Conventional Commits](https://www.conventionalcommits.org/) :

```
type(scope): description

[body optionnel]

[footer optionnel]
```

### Types de commit

- `feat`: Nouvelle fonctionnalité
- `fix`: Correction de bug
- `docs`: Documentation
- `style`: Formatage, style
- `refactor`: Refactoring
- `test`: Ajout de tests
- `chore`: Maintenance

### Exemples

```bash
feat(agents): ajouter agent patrimoine OCR
fix(api): corriger calcul micro-BIC
docs(readme): mettre à jour guide installation
test(fiscal): ajouter tests calculs amortissements
```

## 🔍 Processus de review

### Avant de soumettre

- [ ] Tests passent
- [ ] Code formaté
- [ ] Documentation mise à jour
- [ ] Pas de conflits avec main
- [ ] Fonctionnalité testée manuellement

### Pull Request

1. **Titre clair** décrivant le changement
2. **Description détaillée** avec contexte
3. **Screenshots** pour les changements UI
4. **Tests** inclus et passants
5. **Documentation** mise à jour si nécessaire

### Template PR

```markdown
## Description
Brève description des changements

## Type de changement
- [ ] Bug fix
- [ ] Nouvelle fonctionnalité
- [ ] Breaking change
- [ ] Documentation

## Tests
- [ ] Tests unitaires ajoutés/mis à jour
- [ ] Tests manuels effectués
- [ ] Tous les tests passent

## Screenshots (si applicable)
[Ajouter des captures d'écran]

## Checklist
- [ ] Code formaté selon les standards
- [ ] Documentation mise à jour
- [ ] Pas de conflits avec main
```

## 🐛 Signaler des bugs

### Avant de signaler

1. **Vérifiez** les issues existantes
2. **Reproduisez** le bug
3. **Testez** sur la dernière version

### Template d'issue

```markdown
## Description du bug
Description claire et concise du problème

## Reproduction
Étapes pour reproduire :
1. Aller à '...'
2. Cliquer sur '...'
3. Voir l'erreur

## Comportement attendu
Ce qui devrait se passer

## Captures d'écran
Si applicable

## Environnement
- OS: [ex. Windows 10]
- Navigateur: [ex. Chrome 91]
- Version: [ex. 1.0.0]

## Informations supplémentaires
Contexte additionnel
```

## ✨ Proposer des fonctionnalités

### Template de feature request

```markdown
## Problème à résoudre
Description du problème ou besoin

## Solution proposée
Description de la solution souhaitée

## Alternatives considérées
Autres solutions envisagées

## Informations supplémentaires
Contexte, mockups, références
```

## 🏗️ Architecture

### Principes

- **Séparation des responsabilités**
- **Code réutilisable**
- **Performance optimisée**
- **Sécurité par design**
- **Accessibilité**

### Patterns

- **Backend** : Repository pattern, Service layer
- **Frontend** : Component composition, Custom hooks
- **API** : RESTful design, Consistent responses

## 📚 Documentation

### Types de documentation

- **README** : Vue d'ensemble et installation
- **API** : Endpoints et exemples
- **Code** : Commentaires et docstrings
- **Utilisateur** : Guides et tutoriels

### Standards

- **Français** pour la documentation utilisateur
- **Anglais** pour les commentaires de code
- **Markdown** pour tous les documents
- **Exemples concrets** dans la documentation API

## 🎯 Roadmap

### Priorités actuelles

1. **Stabilité** - Correction des bugs critiques
2. **Performance** - Optimisation des temps de réponse
3. **Fonctionnalités** - Agents IA avancés
4. **UX** - Amélioration de l'interface

### Contributions recherchées

- 🔍 **Tests automatisés** pour améliorer la couverture
- 🎨 **Composants UI** réutilisables
- 🤖 **Agents IA** spécialisés
- 📱 **Responsive design** amélioré
- 🔐 **Sécurité** renforcée

## 💬 Communication

### Canaux

- **GitHub Issues** : Bugs et features
- **GitHub Discussions** : Questions générales
- **Email** : support@lmnp-saas.com

### Code de conduite

- **Respectueux** envers tous les contributeurs
- **Constructif** dans les critiques
- **Collaboratif** dans l'approche
- **Inclusif** dans les discussions

## 🏆 Reconnaissance

Les contributeurs sont reconnus dans :

- **README** principal
- **CHANGELOG** des releases
- **Page About** de l'application
- **Crédits** de la documentation

## 📄 Licence

En contribuant, vous acceptez que vos contributions soient sous licence MIT.

---

Merci de contribuer à LMNP SAAS ! 🚀

