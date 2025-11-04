# Guide de contribution - Shelf MCP Server

Merci de votre intérêt pour contribuer au Shelf MCP Server ! 🎉

## 📋 Table des matières

1. [Code de conduite](#code-de-conduite)
2. [Comment contribuer](#comment-contribuer)
3. [Configuration de développement](#configuration-de-développement)
4. [Guidelines de code](#guidelines-de-code)
5. [Process de soumission](#process-de-soumission)
6. [Reporting de bugs](#reporting-de-bugs)

---

## 🤝 Code de conduite

En participant à ce projet, vous acceptez de maintenir un environnement respectueux et accueillant pour tous. Soyez :

- **Respectueux** - Traitez les autres avec respect
- **Constructif** - Offrez des critiques constructives
- **Patient** - Nous sommes tous ici pour apprendre
- **Inclusif** - Tout le monde est bienvenu

---

## 💡 Comment contribuer

### Types de contributions acceptées

- 🐛 **Bug fixes** - Corrections de bugs
- ✨ **Nouvelles fonctionnalités** - Nouveaux outils ou capacités
- 📝 **Documentation** - Améliorations de la doc
- 🎨 **Améliorations UX** - Meilleurs messages d'erreur, etc.
- ⚡ **Performance** - Optimisations
- 🧪 **Tests** - Ajout de tests

### Ce qui n'est PAS accepté

- ❌ Changements qui cassent l'API existante (sans discussion)
- ❌ Code qui ne suit pas les guidelines
- ❌ Features sans tests ou documentation
- ❌ Dépendances lourdes non justifiées

---

## 🛠️ Configuration de développement

### Prérequis

```bash
# Python 3.10+
python --version

# Git
git --version

# Smithery CLI (optionnel mais recommandé)
npm install -g @smithery/cli
```

### Setup

```bash
# 1. Fork le repository sur GitHub

# 2. Clone votre fork
git clone https://github.com/VOTRE_USERNAME/shelf-mcp-server
cd shelf-mcp-server

# 3. Ajouter le repo upstream
git remote add upstream https://github.com/ORIGINAL_OWNER/shelf-mcp-server

# 4. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 5. Installer les dépendances
pip install -r requirements.txt

# 6. Installer les dépendances de dev (optionnel)
pip install pytest black flake8 mypy

# 7. Configurer l'API key de test
export SHELF_API_KEY="your-test-key"
```

### Tester localement

```bash
# Vérifier la syntaxe
python -m py_compile shelf_mcp_server.py

# Lancer le serveur
python shelf_mcp_server.py

# Dans un autre terminal, tester avec smithery
smithery dev
```

---

## 📝 Guidelines de code

### Style Python

Nous suivons [PEP 8](https://pep8.org/) avec quelques ajustements :

```python
# ✅ Bon
def get_user_history(
    user_id: str,
    time_range: str = "week",
    limit: int = 50
) -> dict[str, Any]:
    """
    Get user's media consumption history.
    
    Args:
        user_id: Unique user identifier
        time_range: Time period to query
        limit: Maximum number of items
        
    Returns:
        Dictionary containing history items
    """
    pass

# ❌ Mauvais
def getUserHistory(userId,timeRange="week",limit=50):
    pass
```

### Type Hints

Toujours utiliser les type hints :

```python
# ✅ Bon
def format_item(item: dict[str, Any]) -> str:
    return f"{item['title']}"

# ❌ Mauvais
def format_item(item):
    return f"{item['title']}"
```

### Docstrings

Format Google style :

```python
def complex_function(param1: str, param2: int) -> bool:
    """
    One-line summary.
    
    More detailed explanation if needed.
    Can span multiple lines.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param2 is negative
        
    Examples:
        >>> complex_function("test", 5)
        True
    """
    pass
```

### Gestion d'erreurs

```python
# ✅ Bon - Messages descriptifs
try:
    response = await make_api_request(endpoint)
except httpx.HTTPStatusError as e:
    if e.response.status_code == 401:
        raise Exception(
            "Authentication failed. Please verify your SHELF_API_KEY. "
            "Contact team@koodos.com if you don't have access."
        )
    raise

# ❌ Mauvais - Messages vagues
try:
    response = await make_api_request(endpoint)
except:
    raise Exception("Error")
```

### Nouveaux outils MCP

Structure à suivre :

```python
@mcp.tool(
    annotations={
        "readOnlyHint": True,  # Si lecture seule
        "destructiveHint": False,  # Si non-destructif
        "idempotentHint": True,  # Si idempotent
        "openWorldHint": True  # Si accès externe
    }
)
async def your_new_tool(params: YourParamsModel) -> str:
    """
    One-line description of what the tool does.
    
    Detailed explanation of the tool's purpose and use cases.
    
    Use cases:
    - Example 1
    - Example 2
    
    Args:
        params: YourParamsModel with field1, field2, etc.
        
    Returns:
        Formatted response in markdown or JSON
        
    Error handling:
        - If X happens, suggests Y
        - If Z error, explains how to fix
    """
    try:
        # Implementation
        pass
    except Exception as e:
        return f"Error: {str(e)}"
```

---

## 🔄 Process de soumission

### 1. Créer une branche

```bash
# Mettre à jour main
git checkout main
git pull upstream main

# Créer une branche feature
git checkout -b feature/nom-de-votre-feature

# Ou pour un bugfix
git checkout -b fix/description-du-bug
```

### 2. Faire vos changements

```bash
# Faire vos modifications

# Tester localement
python -m py_compile shelf_mcp_server.py
python shelf_mcp_server.py

# (Optionnel) Formatter le code
black shelf_mcp_server.py

# (Optionnel) Linter
flake8 shelf_mcp_server.py
```

### 3. Commit

```bash
# Ajouter les fichiers
git add .

# Commit avec un message descriptif
git commit -m "feat: add new search filter option"

# Suivez Conventional Commits:
# feat: Nouvelle fonctionnalité
# fix: Correction de bug
# docs: Documentation
# style: Formatage
# refactor: Refactoring
# test: Tests
# chore: Maintenance
```

### 4. Push et Pull Request

```bash
# Push vers votre fork
git push origin feature/nom-de-votre-feature

# Aller sur GitHub et créer une Pull Request
# Remplir le template de PR avec toutes les informations
```

### 5. Review process

- Les maintainers vont review votre PR
- Répondez aux commentaires et questions
- Faites les changements demandés
- Une fois approuvé, votre PR sera merged !

---

## 🐛 Reporting de bugs

### Avant de reporter

1. **Cherchez** si le bug a déjà été reporté
2. **Vérifiez** que vous êtes sur la dernière version
3. **Testez** avec l'exemple minimal de reproduction

### Template de bug report

```markdown
**Description**
Description claire du bug.

**Pour reproduire**
Étapes pour reproduire :
1. Faire X
2. Faire Y
3. Voir l'erreur

**Comportement attendu**
Ce qui devrait se passer.

**Comportement actuel**
Ce qui se passe réellement.

**Screenshots/Logs**
Si applicable, ajoutez des captures d'écran ou logs.

**Environnement**
- OS: [e.g. macOS 14.0]
- Python version: [e.g. 3.11.5]
- MCP Client: [e.g. Claude Desktop 1.0]
- Version du serveur: [e.g. 1.0.0]

**Contexte additionnel**
Tout autre contexte utile.
```

---

## 🎯 Roadmap des contributions

### Features prioritaires

- [ ] Support HTTP transport (en plus de STDIO)
- [ ] Cache local pour réduire les appels API
- [ ] Support des friends/social features de Shelf
- [ ] Recommendations ML basées sur l'historique
- [ ] Export de données en multiples formats
- [ ] Webhooks pour les mises à jour en temps réel

### Documentation nécessaire

- [ ] Tutoriel vidéo d'installation
- [ ] Plus d'exemples d'utilisation
- [ ] Guide d'architecture détaillé
- [ ] API reference complète

### Tests à ajouter

- [ ] Tests unitaires pour chaque tool
- [ ] Tests d'intégration
- [ ] Tests de performance
- [ ] Tests de sécurité

---

## 📞 Questions ?

- **Discord Smithery** : [discord.gg/Afd38S5p9A](https://discord.gg/Afd38S5p9A)
- **GitHub Discussions** : [Discussions](https://github.com/YOUR_USERNAME/shelf-mcp-server/discussions)
- **Email** : your-email@example.com

---

## 🙏 Remerciements

Merci à tous les contributeurs qui rendent ce projet meilleur ! 

Votre nom sera ajouté au [Contributors](https://github.com/YOUR_USERNAME/shelf-mcp-server/graphs/contributors) une fois votre PR mergée.

---

**Happy coding! 🚀**
