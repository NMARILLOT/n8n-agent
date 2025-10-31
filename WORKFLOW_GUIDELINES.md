# 📋 Guidelines pour les Workflows n8n

Ce document définit les bonnes pratiques et règles à suivre lors de la création ou modification de workflows n8n.

---

## 🎯 Principe Central

**Chaque workflow doit être auto-documenté et compréhensible sans avoir besoin de lire le code JSON brut.**

---

## ✍️ Documentation dans les Workflows

### Règle Obligatoire

**TOUJOURS ajouter des notes (`notes` field) dans les nodes pour expliquer leur rôle et comportement.**

### Quand Ajouter des Notes

✅ **Systématiquement sur:**
- Nodes complexes (Code, Function, expressions avancées)
- Nodes avec logique métier importante
- Nodes de transformation de données
- Nodes conditionnels (Switch, IF)
- Nodes d'intégration externe (API calls, Notion, etc.)
- Nodes critiques ou sensibles (Delete, Update, etc.)

### Format des Notes

#### 🎨 Utiliser des Emojis pour la Clarté Visuelle

Les emojis rendent les notes immédiatement reconnaissables dans l'interface n8n:

**Par Type d'Opération:**
- 📝 Notes générales, description
- ⚙️ Configuration, paramètres
- 🔍 Recherche, filtrage
- ✅ Validation, vérification
- 🔄 Transformation, formatage
- 📊 Agrégation, calculs
- 🚀 Déclenchement, trigger
- 💾 Sauvegarde, création
- ✏️ Modification, update
- 🗑️ Suppression, delete
- ⚠️ Attention, warning
- 🐛 Debug, temporaire
- 🔗 Connexion, liaison
- 📤 Envoi, output
- 📥 Réception, input

#### 📐 Structure Recommandée

```
[EMOJI] Titre court et clair

Description détaillée sur 1-3 lignes expliquant:
- Ce que fait le node
- Pourquoi c'est important
- Cas particuliers ou edge cases
```

#### ✨ Exemples de Bonnes Notes

**Node Code de recherche:**
```
🔍 Recherche et formate les idées par mots-clés

Filtre les idées de la database Notion par correspondance
dans le titre ou le contenu. Retourne un format lisible
pour l'agent IA.
```

**Node Notion Update:**
```
✏️ Met à jour une idée existante dans Notion

ATTENTION: Merge les nouvelles valeurs avec les anciennes.
Les champs non fournis conservent leur valeur actuelle.
```

**Node Switch:**
```
🔀 Route vers l'opération demandée

Analyse le champ 'operation' et dirige vers:
- search_ideas → Recherche
- update_idea → Modification
- delete_idea → Suppression
- etc.
```

**Node de suppression:**
```
⚠️🗑️ Suppression DÉFINITIVE de l'idée

Action IRRÉVERSIBLE. L'idée est supprimée de Notion
sans possibilité de récupération. Toujours confirmer
avec l'utilisateur avant d'exécuter.
```

---

## 🏗️ Organisation des Workflows

### Structure Claire et Visuelle

**RÈGLE D'OR : Un workflow = Un schéma compréhensible par un enfant de 10 ans**

### 🎨 Disposition Visuelle OBLIGATOIRE

1. **Flux de gauche à droite** - TOUJOURS suivre le sens de lecture naturel
2. **Espacement généreux** - 200px minimum entre chaque node
3. **Alignement parfait** - Nodes au même niveau = même position Y (alignés horizontalement)
4. **Groupage visuel** - Nodes liés = proches visuellement (max 300px de distance)
5. **Pas de croisement de lignes** - Les connexions ne doivent JAMAIS se croiser
6. **Branches parallèles** - Espacées de 300px minimum verticalement

### 📐 Grille de Positionnement

Utiliser une grille mentale de **200px** :
- **X** : 0, 200, 400, 600, 800, 1000, 1200, 1400, 1600
- **Y** : -400, -200, 0, 200, 400, 600, 800

### 🏷️ Sticky Notes OBLIGATOIRES

**Quand ajouter des Sticky Notes :**
- ✅ Au début du workflow (explication générale)
- ✅ Avant chaque section logique (groupe de nodes)
- ✅ Aux points de décision (Switch, IF)
- ✅ Avant les boucles ou logiques complexes
- ✅ Aux points d'intégration externe (API, MCP)

**Format des Sticky Notes :**
```
📌 [EMOJI] TITRE COURT ET CLAIR

Explication simple comme pour un enfant de 10 ans.
Utilise des phrases courtes et directes.

✅ Ce qui se passe ici
❌ Ce qui NE se passe PAS
```

**Emojis recommandés pour Sticky Notes :**
- 🚀 Début du workflow
- 📥 Réception de données
- 🔀 Décision / Choix
- ⚙️ Traitement / Transformation
- 📤 Envoi de données
- ✅ Résultat / Succès
- ⚠️ Attention / Important

### 📏 Exemple de Disposition Parfaite

```
Sticky Note (0, -200)
┌─────────────────────────────────┐
│ 🚀 DÉBUT DU WORKFLOW            │
│                                 │
│ Ce workflow capture les idées   │
│ depuis Telegram (texte ou vocal)│
└─────────────────────────────────┘

Trigger (200, 0) → Switch (400, 0)
                      ├─ Vocal (600, -200) → ... → Merge (1400, 0)
                      └─ Texte (600, 200)  → ... → Merge (1400, 0)

Sticky Note (1200, -400)
┌─────────────────────────────────┐
│ 🔀 FUSION DES 2 BRANCHES        │
│                                 │
│ Une seule branche s'exécute,    │
│ le Merge reçoit les données.    │
└─────────────────────────────────┘
```

### 🎯 Checklist Visuelle Avant Déploiement

- [ ] **Espacement** : Tous les nodes espacés de 200px minimum
- [ ] **Alignement** : Nodes parallèles alignés horizontalement
- [ ] **Flux** : Lecture de gauche à droite sans confusion
- [ ] **Pas de croisement** : Aucune ligne ne se croise
- [ ] **Sticky Notes** : Au moins 3 sticky notes explicatives
- [ ] **Notes nodes** : Tous les nodes importants ont des notes avec emojis
- [ ] **Noms clairs** : Pas de "Node1", "Code", "HTTP Request" génériques

### Naming Convention

**Nodes:**
- Nom descriptif et explicite
- Format: `[Type] - [Action]` (ex: "Notion - Search Ideas", "Code - Format Response")
- Éviter les noms génériques comme "Node1", "Code", "HTTP Request"

**Variables:**
- camelCase pour JavaScript
- snake_case pour les champs Notion
- Noms parlants (pas de `temp`, `data`, `result` génériques)

---

## 🔧 Bonnes Pratiques Techniques

### Code Nodes

✅ **Toujours:**
- Commenter le code complexe
- Gérer les cas d'erreur (null, undefined)
- Retourner des formats cohérents
- Valider les inputs

❌ **Éviter:**
- Code non commenté de plus de 10 lignes
- Logique métier complexe sans documentation
- Mutations d'objets globaux

### Expressions n8n

✅ **Préférer:**
- Expressions simples et lisibles
- Utiliser `$json.field` plutôt que chaînes complexes
- Ajouter des commentaires pour logique complexe

### Error Handling

✅ **Systématique:**
- Try/Catch dans Code nodes critiques
- Validation des inputs API
- Messages d'erreur clairs pour l'utilisateur
- Fallbacks ou comportements par défaut

---

## 🎯 Checklist Avant Commit

Avant de sauvegarder/déployer un workflow:

- [ ] Tous les nodes importants ont des notes
- [ ] Les notes utilisent des emojis appropriés
- [ ] Les noms de nodes sont descriptifs
- [ ] Le flux est organisé visuellement
- [ ] Les erreurs sont gérées
- [ ] Le code complexe est commenté
- [ ] Les credentials sont configurés
- [ ] Le workflow a été testé

---

## 📚 Exemples Réels

### ✅ Bon Exemple

```json
{
  "name": "Notion - Search Ideas",
  "notes": "🔍 Recherche toutes les idées dans la database\n\nRécupère ALL les idées pour permettre le filtrage\nlocal par mots-clés. Plus performant que les filtres\nNotion pour des recherches textuelles."
}
```

### ❌ Mauvais Exemple

```json
{
  "name": "Notion1",
  "notes": ""
}
```

---

## 🔄 Maintenance et Évolution

### Mise à Jour des Notes

- Mettre à jour les notes lors de modifications de logique
- Supprimer les notes obsolètes (marquées 🐛 DEBUG par exemple)
- Enrichir les notes en fonction des bugs découverts

### Documentation Externe

Les notes dans les workflows NE REMPLACENT PAS:
- Le README.md du système (vue d'ensemble)
- La documentation API/technique
- Les guides utilisateur

Mais elles COMPLÈTENT ces documents en fournissant le contexte immédiat dans le workflow.

---

## 📐 Template de Node

Lors de la création d'un nouveau node important:

```python
{
  "parameters": { ... },
  "type": "...",
  "name": "[Type] - [Action Claire]",
  "notes": "[EMOJI] Titre court\n\nDescription détaillée.\nCas particuliers ou warnings.",
  "position": [x, y],
  "id": "..."
}
```

---

## 🎓 Philosophie

> "Un workflow bien documenté est un workflow qui se maintient tout seul."
>
> "Si tu dois ouvrir le code pour comprendre, c'est que la note est insuffisante."
>
> "Les emojis ne sont pas de la décoration, ils sont de la communication visuelle."

---

## ✨ Résumé

1. **TOUJOURS** ajouter des notes avec emojis dans les nodes
2. **TOUJOURS** utiliser des noms descriptifs
3. **TOUJOURS** organiser visuellement le workflow
4. **TOUJOURS** gérer les erreurs
5. **TOUJOURS** penser UX/UI dans la disposition

**Un bon workflow = Un workflow qu'on comprend en 30 secondes en le regardant visuellement.**
