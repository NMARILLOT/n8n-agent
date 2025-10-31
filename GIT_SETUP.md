# 📦 Git & GitHub Setup Guide

Guide pour configurer le versioning GitHub et maintenir l'historique des déploiements.

---

## ✅ État Actuel

Le projet est maintenant configuré avec:

- ✅ Dépôt Git local initialisé
- ✅ `.gitignore` configuré (ignore `.env`, `node_modules`, logs, etc.)
- ✅ Commit initial créé avec tous les fichiers
- ✅ Auto-commit avant chaque déploiement

---

## 🚀 Connexion à GitHub

### Étape 1: Créer le dépôt sur GitHub

1. Va sur https://github.com/new
2. Nom du dépôt: `n8n-agent` (ou autre nom de ton choix)
3. Description: "Automated n8n workflow management with API integration"
4. **Important**: Ne pas initialiser avec README, .gitignore ou licence (on a déjà tout)
5. Clique sur "Create repository"

### Étape 2: Connecter le dépôt local

Après création, GitHub te donne des commandes. Utilise celles-ci:

```bash
# Ajouter le remote GitHub
git remote add origin https://github.com/TON_USERNAME/n8n-agent.git

# Ou avec SSH si tu as configuré les clés SSH
git remote add origin git@github.com:TON_USERNAME/n8n-agent.git

# Renommer la branche en main (si nécessaire)
git branch -M main

# Pousser le commit initial
git push -u origin main
```

### Étape 3: Vérifier la connexion

```bash
# Vérifier le remote
git remote -v

# Devrait afficher:
# origin  https://github.com/TON_USERNAME/n8n-agent.git (fetch)
# origin  https://github.com/TON_USERNAME/n8n-agent.git (push)
```

---

## 🔄 Workflow de Déploiement avec Versioning

### Fonctionnement Automatique

Chaque fois que tu lances `./scripts/deploy.sh`, le système va automatiquement:

1. **Vérifier s'il y a des changements** dans les workflows
2. **Créer un commit automatique** avec:
   - Timestamp exact
   - Workflows déployés (tous ou un système spécifique)
   - Mode (production ou dry-run)
3. **Afficher le hash du commit** pour référence
4. **Te rappeler de push vers GitHub**
5. **Puis déployer sur n8n**

### Exemple de Workflow

```bash
# 1. Tu modifies des workflows localement
nano "Agent Telegram - Dev Nico Perso/workflow/Agent Telegram - Dev Ideas.json"

# 2. Tu déploies (commit automatique avant déploiement)
./scripts/deploy.sh --dir "Agent Telegram - Dev Nico Perso"

# Sortie:
# 📦 Git Versioning...
# ✅ Committed changes: a1b3cbc
# 💡 Push to GitHub: git push origin main
#
# 🚀 Starting deployment...
# ✅ Deployed successfully!

# 3. Tu push vers GitHub pour sauvegarder
git push origin main
```

---

## 📚 Historique et Navigation

### Voir l'historique des déploiements

```bash
# Voir tous les commits de déploiement
git log --oneline --grep="Pre-deployment"

# Voir les détails d'un déploiement spécifique
git show a1b3cbc

# Voir les changements d'un workflow
git log --follow -- "Agent Telegram - Dev Nico Perso/workflow/Agent Telegram - Dev Ideas.json"
```

### Revenir en arrière si nécessaire

```bash
# Voir les différences entre maintenant et un commit précédent
git diff a1b3cbc HEAD -- "Agent Telegram - Dev Nico Perso/workflow/"

# Récupérer une ancienne version d'un workflow
git checkout a1b3cbc -- "Agent Telegram - Dev Nico Perso/workflow/Agent Telegram - Dev Ideas.json"

# Puis redéployer si besoin
./scripts/deploy.sh --dir "Agent Telegram - Dev Nico Perso"
```

---

## 🎯 Bonnes Pratiques

### Synchronisation Régulière

```bash
# Après chaque déploiement, push vers GitHub
git push origin main

# Ou configure l'auto-push en ajoutant à deploy.sh (optionnel)
# git push origin main (après le commit automatique)
```

### Branches pour Expérimentation

```bash
# Créer une branche pour tester de nouveaux workflows
git checkout -b feature/nouveau-bot-telegram

# Modifier et tester
nano "Nouveau Bot/workflow/bot.json"
./scripts/deploy.sh --dry-run --dir "Nouveau Bot"

# Si ça marche, merger dans main
git checkout main
git merge feature/nouveau-bot-telegram
git push origin main
```

### Tags pour Versions Importantes

```bash
# Créer un tag pour une version stable
git tag -a v1.0.0 -m "Version 1.0.0 - Production stable"

# Pousser le tag
git push origin v1.0.0

# Lister tous les tags
git tag -l
```

---

## 🔍 Messages de Commit

### Format Automatique

Les commits créés automatiquement suivent ce format:

```
Pre-deployment snapshot: [target]

Timestamp: 2025-10-31 14:30:45
Target: Agent Telegram - Dev Nico Perso
Mode: production

🤖 Automated commit before n8n deployment

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Commits Manuels Additionnels

Tu peux aussi faire des commits manuels pour documenter d'autres changements:

```bash
# Après avoir modifié la documentation
git add README.md CLAUDE.md
git commit -m "Update documentation with new workflow examples"
git push origin main
```

---

## 🛡️ Sécurité

### Ce qui N'est PAS versionné

Le `.gitignore` protège automatiquement:

- ❌ `.env` - Contient les clés API (JAMAIS versionné)
- ❌ `node_modules/` - Dépendances (reconstruites à partir de package.json)
- ❌ `*.log` - Fichiers de logs
- ❌ Fichiers temporaires et backup

### Vérifier avant de Push

```bash
# Toujours vérifier ce qui va être poussé
git status
git diff origin/main

# Si tu vois .env ou des secrets, STOP!
# Ajouter au .gitignore et recommencer
```

---

## 🚨 Troubleshooting

### Erreur: "remote origin already exists"

```bash
# Voir le remote actuel
git remote -v

# Le supprimer si c'est le mauvais
git remote remove origin

# Ajouter le bon
git remote add origin https://github.com/TON_USERNAME/n8n-agent.git
```

### Erreur: "failed to push"

```bash
# Récupérer les changements distants d'abord
git pull origin main --rebase

# Puis push
git push origin main
```

### Annuler le dernier commit (si erreur)

```bash
# Annuler le dernier commit mais garder les changements
git reset --soft HEAD~1

# Annuler le dernier commit ET les changements (DANGER!)
git reset --hard HEAD~1
```

---

## 📊 Commandes Utiles

```bash
# Voir l'état actuel
git status

# Voir l'historique graphique
git log --oneline --graph --all --decorate

# Voir les fichiers modifiés dans le dernier commit
git show --name-only

# Rechercher dans l'historique
git log -S "recherche_texte"

# Voir qui a modifié chaque ligne d'un fichier
git blame "fichier.json"
```

---

## 🎓 Prochaines Étapes

1. **Créer le dépôt GitHub** (voir Étape 1)
2. **Connecter le remote** (voir Étape 2)
3. **Push le commit initial** (`git push -u origin main`)
4. **Déployer un workflow** (`./scripts/deploy.sh`)
5. **Observer le commit automatique**
6. **Push vers GitHub** (`git push origin main`)

---

## 📖 Ressources

- [GitHub Documentation](https://docs.github.com/)
- [Git Cheat Sheet](https://training.github.com/downloads/github-git-cheat-sheet/)
- [Pro Git Book](https://git-scm.com/book/en/v2) (gratuit)

---

**Créé le**: 2025-10-31
**Maintenu par**: Claude Code + Nicolas Marillot
