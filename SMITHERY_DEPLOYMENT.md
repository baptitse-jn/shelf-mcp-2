# Guide de déploiement Smithery - Shelf MCP Server

Ce guide explique comment publier votre serveur MCP Shelf sur Smithery, étape par étape.

## 📋 Table des matières

1. [Prérequis](#prérequis)
2. [Préparation du repository](#préparation-du-repository)
3. [Configuration Smithery](#configuration-smithery)
4. [Déploiement](#déploiement)
5. [Vérification](#vérification)
6. [Publication](#publication)
7. [Maintenance](#maintenance)

---

## 🎯 Prérequis

### Comptes requis

- [ ] **Compte GitHub** - Pour héberger le code
- [ ] **Compte Smithery** - Créer sur [smithery.ai](https://smithery.ai)
- [ ] **API Key Shelf** - Obtenir via team@koodos.com

### Outils nécessaires

```bash
# Node.js (pour Smithery CLI)
node --version  # Doit être >= 14

# Python
python --version  # Doit être >= 3.10

# Git
git --version

# Smithery CLI
npm install -g @smithery/cli
```

### Vérification

```bash
# Vérifier l'installation de Smithery CLI
smithery --version

# Login à Smithery
smithery login
# Suivez les instructions pour vous authentifier
```

---

## 📦 Préparation du repository

### 1. Structure du projet

Votre repository doit avoir cette structure :

```
shelf-mcp-server/
├── shelf_mcp_server.py          # Le serveur MCP
├── requirements.txt              # Dépendances Python
├── smithery.yaml                 # Config Smithery ⭐
├── Dockerfile                    # Pour containerisation
├── .dockerignore                 # Exclusions Docker
├── README.md                     # Documentation principale
├── README_SMITHERY.md            # Documentation Smithery
└── LICENSE                       # Licence (recommandé)
```

### 2. Créer le repository GitHub

```bash
# Créer un nouveau repository sur GitHub
# Nommez-le: shelf-mcp-server

# Cloner localement
git clone https://github.com/VOTRE_USERNAME/shelf-mcp-server
cd shelf-mcp-server

# Copier tous les fichiers nécessaires
cp /path/to/shelf_mcp_server.py .
cp /path/to/requirements.txt .
cp /path/to/smithery.yaml .
cp /path/to/Dockerfile .
cp /path/to/.dockerignore .
cp /path/to/README_SMITHERY.md ./README.md

# Commit initial
git add .
git commit -m "Initial commit: Shelf MCP Server"
git push origin main
```

### 3. Ajouter une licence

```bash
# Créer un fichier LICENSE (MIT recommandé)
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2025 [Votre Nom]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

git add LICENSE
git commit -m "Add MIT license"
git push
```

---

## ⚙️ Configuration Smithery

### 1. Vérifier smithery.yaml

Le fichier `smithery.yaml` doit être à la racine du repo :

```yaml
startCommand:
  type: http
  httpServer:
    port: 8000
    healthCheckPath: /healthz
  configSchema:
    type: object
    required:
      - shelfApiKey
    properties:
      shelfApiKey:
        type: string
        title: "Shelf API Key"
        description: "Your Shelf.im API key"
      apiBaseUrl:
        type: string
        title: "API Base URL"
        default: "https://api.shelf.im/v1"

  commandFunction: |
    (config) => {
      const port = 8000;
      return {
        command: 'python',
        args: [
          'shelf_mcp_server.py',
          '--transport', 'streamable-http',
          '--host', '0.0.0.0',
          '--port', String(port)
        ],
        env: {
          SHELF_API_KEY: config.shelfApiKey,
          SHELF_API_BASE_URL: config.apiBaseUrl || 'https://api.shelf.im/v1',
          MCP_TRANSPORT: 'streamable-http',
          MCP_HOST: '0.0.0.0',
          MCP_PORT: String(port)
        }
      };
    }
```

> 💡 Pour les tests locaux avec le SDK MCP en mode stdio, lancez le serveur avec `python shelf_mcp_server.py --transport stdio`.


### 2. Tester localement

Avant de déployer, testez que tout fonctionne :

```bash
# Installer les dépendances
pip install -r requirements.txt

# Définir l'API key de test
export SHELF_API_KEY="your-test-key"

# Lancer le serveur HTTP (transport requis par Smithery)
python shelf_mcp_server.py --transport streamable-http --host 0.0.0.0 --port 8000 &
SERVER_PID=$!

# Le serveur devrait démarrer sans erreur
# Ctrl+C pour arrêter

# Tuer le processus
kill $SERVER_PID
```

### 3. Tester avec Smithery dev mode

```bash
# Démarrer le serveur en mode dev
smithery dev

# Dans un autre terminal, tester
smithery run shelf --config '{"shelfApiKey":"your-key"}'
```

---

## 🚀 Déploiement

### Option 1 : Déploiement via Smithery CLI

```bash
# S'assurer d'être dans le repo
cd shelf-mcp-server

# S'assurer d'être logged in
smithery login

# Déployer
smithery deploy

# Suivre les instructions interactives
# Smithery va :
# 1. Valider smithery.yaml
# 2. Builder le container (si nécessaire)
# 3. Déployer sur leur infrastructure
# 4. Vous donner une URL de serveur
```

### Option 2 : Déploiement via Smithery Dashboard

1. **Aller sur smithery.ai**
2. **Cliquer sur "Add Server"**
3. **Connecter votre repo GitHub**
   - Autoriser Smithery à accéder à votre repo
   - Sélectionner `shelf-mcp-server`
4. **Configuration automatique**
   - Smithery détecte `smithery.yaml`
   - Valide la configuration
5. **Déployer**
   - Cliquer sur "Deploy"
   - Attendre le build (~2-5 minutes)

### Logs de déploiement

```bash
# Voir les logs en temps réel
smithery logs shelf

# Ou via le dashboard
# smithery.ai/servers/shelf/logs
```

---

## ✅ Vérification

### 1. Vérifier le déploiement

```bash
# Lister vos serveurs
smithery list

# Devrait montrer :
# shelf - Active - v1.0.0
```

### 2. Tester l'installation

```bash
# Installer votre serveur localement depuis Smithery
smithery install shelf --client claude

# Tester avec Claude Desktop
# Ouvrir Claude et essayer :
# "Use the Shelf server to show me what I watched this week"
```

### 3. Playground Smithery

1. Aller sur `smithery.ai/servers/shelf`
2. Cliquer sur "Playground"
3. Tester les outils interactivement
4. Vérifier que tout fonctionne

---

## 📢 Publication

### 1. Rendre public

Par défaut, votre serveur est privé. Pour le rendre public :

```bash
# Via CLI
smithery publish shelf

# Ou via dashboard
# smithery.ai/servers/shelf/settings
# Toggle "Public" → ON
```

### 2. Optimiser la page

Sur le dashboard Smithery, configurez :

- **Description courte** : "Access your Shelf.im cultural consumption data"
- **Tags** : `media`, `movies`, `music`, `books`, `personal-data`
- **Catégorie** : `Data & Analytics`
- **Logo** : (optionnel) Uploader un logo 512x512
- **Screenshots** : Ajouter des captures d'écran d'utilisation

### 3. Documentation

Assurez-vous que `README.md` est clair et complet :

```bash
# Le README doit inclure :
- Description claire
- Instructions d'installation
- Exemples d'utilisation
- Configuration requise
- Troubleshooting
```

### 4. Annonce

Une fois publié, annoncez-le :

- **Twitter/X** : Tweetez avec #MCP #Smithery #ShelfIM
- **Discord Smithery** : Partagez dans #showcase
- **Reddit** : r/LocalLLaMA, r/ClaudeAI
- **LinkedIn** : Post professionnel

---

## 🔄 Maintenance

### Mises à jour

```bash
# Faire des changements dans le code
vim shelf_mcp_server.py

# Commit et push
git add .
git commit -m "feat: add new feature"
git push

# Déployer la nouvelle version
smithery deploy

# Smithery va automatiquement :
# 1. Détecter les changements
# 2. Builder la nouvelle version
# 3. Déployer avec un nouveau numéro de version
```

### Versioning

Smithery utilise le versioning sémantique :

- **v1.0.0** → **v1.0.1** : Bug fixes
- **v1.0.0** → **v1.1.0** : Nouvelles fonctionnalités
- **v1.0.0** → **v2.0.0** : Breaking changes

```bash
# Pour forcer une version spécifique
smithery deploy --version 1.1.0
```

### Monitoring

```bash
# Voir les stats d'utilisation
smithery stats shelf

# Voir les logs en temps réel
smithery logs shelf --follow

# Voir les erreurs
smithery logs shelf --level error
```

### Support utilisateur

Créez un fichier `SUPPORT.md` :

```markdown
# Support

## Getting Help

- **Discord**: [Join Smithery Discord](https://discord.gg/...)
- **Email**: your-email@example.com
- **GitHub Issues**: [Report a bug](https://github.com/YOU/shelf-mcp-server/issues)

## Common Issues

[Link to troubleshooting section]
```

---

## 📊 Métriques de succès

Une fois publié, suivez ces métriques sur le dashboard :

- **Installations** : Nombre d'utilisateurs
- **Appels d'outils** : Utilisation des fonctionnalités
- **Évaluations** : Retours utilisateurs
- **Stars GitHub** : Popularité du projet

### Objectifs

- ✅ 10 installations - Semaine 1
- ✅ 50 installations - Mois 1
- ✅ 100 installations - Mois 3
- ✅ 1000 appels d'outils - Mois 1

---

## 🐛 Debugging

### Problèmes courants

#### "Build failed"

```bash
# Vérifier les logs de build
smithery logs shelf --build

# Tester le build Docker localement
docker build -t shelf-mcp-test .
docker run shelf-mcp-test
```

#### "Server not responding"

```bash
# Vérifier que le serveur démarre
python shelf_mcp_server.py --transport streamable-http --host 0.0.0.0 --port 8000

# Vérifier les dépendances
pip install -r requirements.txt --dry-run
```

#### "Configuration validation failed"

```bash
# Valider smithery.yaml localement
smithery validate

# Tester avec une config de test
smithery run shelf --config '{"shelfApiKey":"test"}'
```

---

## 📚 Ressources supplémentaires

### Documentation

- [Smithery Docs](https://smithery.ai/docs)
- [MCP Specification](https://modelcontextprotocol.io)
- [FastMCP Guide](https://github.com/modelcontextprotocol/python-sdk)

### Exemples

- [Smithery Reference Servers](https://github.com/smithery-ai/reference-servers)
- [MCP Servers Repo](https://github.com/smithery-ai/mcp-servers)

### Communauté

- **Discord Smithery** : Support et discussions
- **GitHub Discussions** : Questions techniques
- **Twitter #MCP** : Nouvelles et annonces

---

## ✅ Checklist finale

Avant de publier, vérifiez :

- [ ] Repository GitHub public
- [ ] `smithery.yaml` correct et testé
- [ ] `README.md` complet et clair
- [ ] `LICENSE` ajoutée
- [ ] Testé localement avec succès
- [ ] Déployé sur Smithery
- [ ] Testé via Playground Smithery
- [ ] Description et tags configurés
- [ ] Serveur rendu public
- [ ] Documentation de support créée
- [ ] Annonce préparée

---

## 🎉 Félicitations !

Votre serveur MCP Shelf est maintenant disponible sur Smithery !

Les utilisateurs peuvent l'installer avec :

```bash
smithery install shelf --client claude
```

**Prochaines étapes :**

1. Surveillez les métriques
2. Répondez aux questions des utilisateurs
3. Itérez basé sur les retours
4. Ajoutez de nouvelles fonctionnalités
5. Partagez votre succès !

---

**Besoin d'aide ?** 

- Discord Smithery : [discord.gg/Afd38S5p9A](https://discord.gg/Afd38S5p9A)
- Email : team@smithery.ai

**Bonne chance avec votre lancement ! 🚀**
