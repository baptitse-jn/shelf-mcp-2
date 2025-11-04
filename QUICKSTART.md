# Quick Start - Shelf MCP Server via Smithery

Installation en 2 minutes pour utiliser le serveur MCP Shelf avec Claude ou d'autres clients IA.

## 🚀 Installation rapide

### Étape 1 : Installer Smithery CLI

```bash
npm install -g @smithery/cli
```

### Étape 2 : Obtenir une API Key Shelf

⚠️ **Important :** L'API Shelf.im est en early access.

1. Envoyez un email à **team@koodos.com**
2. Sujet : "Shelf API Access Request"
3. Mentionnez que vous voulez utiliser le MCP Server
4. Attendez 3-7 jours pour la réponse

### Étape 3 : Installer le serveur

```bash
# Pour Claude Desktop
smithery install shelf --client claude

# Pour Cursor
smithery install shelf --client cursor

# Pour d'autres clients
smithery install shelf
```

### Étape 4 : Configuration

Quand demandé, entrez :

1. **Shelf API Key** : [Votre clé reçue de Koodos]
2. **API Base URL** : [Laisser par défaut ou appuyez sur Entrée]

### Étape 5 : Redémarrer votre client

- **Claude Desktop** : Quittez et relancez complètement
- **Cursor** : Redémarrez l'éditeur

## ✅ Vérification

Testez que ça fonctionne :

**Dans Claude :**
```
"Use the Shelf server to show me what I watched this week"
```

**Dans Cursor :**
```
// Demandez à l'assistant de query votre Shelf
"What music have I been listening to on Shelf?"
```

## 💡 Exemples d'utilisation

### Requêtes basiques

```
"What did I watch on Shelf yesterday?"
"Show me my music history from this month"
"Have I read any sci-fi books recently?"
```

### Analyses

```
"Analyze my movie taste over the last 3 months"
"What genres do I listen to most?"
"How has my reading changed this year?"
```

### Recommandations

```
"Based on my Shelf history, recommend a movie"
"Suggest music similar to what I've been listening to"
"What's trending on Shelf that I might like?"
```

## 🛠️ Commandes utiles

```bash
# Lister les serveurs installés
smithery list

# Voir les détails du serveur Shelf
smithery inspect shelf

# Désinstaller
smithery uninstall shelf

# Réinstaller (si problème)
smithery uninstall shelf && smithery install shelf
```

## 🆘 Problèmes courants

### "Authentication failed"

**Solution :** Vérifiez votre API key

```bash
# Réinstaller avec la bonne clé
smithery uninstall shelf
smithery install shelf
```

### "Server not found"

**Solution :** Le serveur n'est peut-être pas encore publié

```bash
# Vérifier le statut
smithery search shelf

# Ou installer depuis GitHub directement
smithery install github.com/your-username/shelf-mcp-server
```

### "No data returned"

**Solution :** Vérifiez que vous avez du contenu sur Shelf

1. Ouvrez l'app Shelf (iOS/Android)
2. Connectez vos comptes (Spotify, Netflix, etc.)
3. Attendez quelques heures pour la synchronisation
4. Réessayez

## 📚 Plus d'informations

- **Documentation complète** : Voir README.md
- **Support** : team@koodos.com
- **Smithery Discord** : [discord.gg/Afd38S5p9A](https://discord.gg/Afd38S5p9A)
- **Shelf.im** : https://www.shelf.im

## 🎯 Les 5 outils disponibles

1. **get_recent_history** - Historique de consommation
2. **search_media_history** - Recherche dans l'historique
3. **get_recap** - Récapitulatifs hebdo/mensuels
4. **get_item_details** - Détails d'un item
5. **get_trending_on_shelf** - Tendances Shelf

## ⭐ Tips & Tricks

### Raccourcis Claude

Au lieu de :
```
"Use the Shelf server to get my recent history"
```

Utilisez :
```
"What did I watch lately?" 
```

Claude comprend le contexte et utilisera automatiquement Shelf !

### Combiner les sources

```
"Compare my Shelf music taste with Spotify Wrapped"
"Show me movies I watched that are also on my Letterboxd"
```

### Contexte temporel

Soyez spécifique sur les dates :
```
"What did I watch last Tuesday?"
"Show me books from Q3 2024"
"Music from my summer vacation"
```

## 🎉 C'est tout !

Vous êtes prêt à utiliser Shelf avec votre IA ! 🚀

---

**Besoin d'aide ?** Rejoignez le [Discord Smithery](https://discord.gg/Afd38S5p9A)
