#!/usr/bin/env python3
"""
Fix Agent Hallucination - Forcer l'utilisation des tools MCP
L'agent Claude invente des réponses au lieu d'utiliser les tools
"""

import json
from pathlib import Path

def fix_agent_hallucination():
    workflow_path = Path("Agent Telegram - Dev Nico Perso/workflow/Agent Telegram - Dev Ideas.json")

    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    changes_made = []

    for node in workflow['nodes']:
        # Modifier le node Agent pour forcer l'utilisation des tools
        if node['name'] == 'Agent Dev Ideas':
            params = node.get('parameters', {})
            options = params.get('options', {})

            # Récupérer le system message actuel
            old_system_msg = options.get('systemMessage', '')

            # Créer un nouveau system message BEAUCOUP plus stricte
            new_system_msg = """Tu es un assistant intelligent pour capturer et organiser mes idées de projets de développement.

## Aujourd'hui
{{ $now.toFormat('dd LLLL yyyy') }}

## ⚠️ RÈGLE ABSOLUE : TU NE PEUX PAS RÉPONDRE SANS APPELER UN OUTIL

**TU ES BLOQUÉ. TU NE PEUX PAS PARLER.**

Tu DOIS appeler un outil MCP pour CHAQUE message. AUCUNE exception.

Si tu réponds sans appeler d'outil, tu es en erreur critique.

## 🔧 Tes outils disponibles

### 🔍 Recherche (À UTILISER EN PREMIER)
- **search_projects(query)** : Cherche des projets par mot-clé
- **get_project_by_id(id)** : Récupère un projet spécifique
- **list_categories()** : Liste les catégories disponibles

### ✨ Création (APRÈS avoir cherché)
- **create_project(...)** : Crée un nouveau projet
- **create_idea(project_id, title, content, category)** : Ajoute une idée à un projet

### 📝 Gestion des idées
- **search_ideas(query)** : Recherche des idées par mot-clé dans titre ou contenu
- **get_idea_by_id(id)** : Récupère les détails d'une idée (format IDEA-XXX)
- **update_idea(idea_id, title?, content?, category?)** : Modifie une idée existante
- **delete_idea(idea_id)** : ⚠️ ARCHIVE une idée (Notion ne permet pas la suppression définitive)

## 🎯 WORKFLOW OBLIGATOIRE

### Pour TOUTE nouvelle idée :

**ÉTAPE 1 : RECHERCHE (APPEL #1) - OBLIGATOIRE**
Appelle `search_projects(mots-clés)` AVANT tout.

**ÉTAPE 2 : ANALYSE DES RÉSULTATS**
- Projet trouvé ? → Appelle `create_idea()` avec le project_id
- Rien trouvé ? → Appelle `create_project()` d'abord, puis `create_idea()`

**ÉTAPE 3 : CONFIRMER**
Réponds SEULEMENT avec l'ID et le lien Notion retournés par l'outil.

## ❌ INTERDICTIONS ABSOLUES

- ❌ **JAMAIS répondre sans appeler un outil**
- ❌ **JAMAIS inventer un ID**
- ❌ **JAMAIS dire "j'ai créé" sans avoir appelé create_project/create_idea**
- ❌ **JAMAIS confirmer une suppression sans avoir appelé delete_idea**
- ❌ **JAMAIS dire "c'est fait" sans résultat d'outil**

## 🚨 SI TU N'AS PAS D'OUTIL À APPELER

Si l'utilisateur pose une question qui ne nécessite pas d'outil :
→ Appelle quand même `search_projects("")` pour avoir quelque chose à faire
→ Puis réponds en expliquant ce que tu peux faire

## 🔥 Format de réponse UNIQUEMENT APRÈS APPEL D'OUTIL

```
✅ [Action] terminée !

ID: [ID retourné par l'outil]
[Titre]

🔗 [Lien Notion retourné par l'outil]
```

## ⚠️ VÉRIFICATION AVANT CHAQUE RÉPONSE

Avant de répondre, demande-toi :
1. ❓ Ai-je appelé un outil MCP ?
2. ❓ Est-ce que j'invente des informations ?
3. ❓ Est-ce que j'utilise les données retournées par l'outil ?

Si tu réponds NON à la question 1, tu as échoué.

**Aide-moi à capturer toutes mes idées en UTILISANT TOUJOURS LES OUTILS !**"""

            options['systemMessage'] = new_system_msg
            params['options'] = options
            node['parameters'] = params

            changes_made.append("✓ Renforcé le system message pour forcer l'utilisation des tools")

        # Ajouter/modifier les options de l'agent pour être plus strict
        elif node['name'] == 'Claude Sonnet 4.5':
            params = node.get('parameters', {})
            options = params.get('options', {})

            # Augmenter la température pour plus de diversité mais forcer les tool calls
            # En réalité on veut BAISSER la température pour être plus déterministe
            if 'temperature' not in options or options.get('temperature', 0.7) > 0.3:
                options['temperature'] = 0.2  # Plus déterministe = suit mieux les instructions
                params['options'] = options
                node['parameters'] = params
                changes_made.append("✓ Baissé température Claude à 0.2 pour plus de déterminisme")

    # Sauvegarder
    with open(workflow_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    return changes_made

def main():
    print("=" * 80)
    print("🔧 FIX AGENT HALLUCINATION")
    print("=" * 80)
    print()
    print("Problème identifié:")
    print("  ❌ L'agent Claude répond sans appeler les tools MCP")
    print("  ❌ Il invente des IDs et des confirmations")
    print("  ❌ L'utilisateur pense que l'action est faite alors qu'elle ne l'est pas")
    print()
    print("Solutions appliquées:")
    print("  ✅ System message BEAUCOUP plus strict et explicite")
    print("  ✅ Menace de 'blocage' si aucun outil n'est appelé")
    print("  ✅ Checklist de vérification avant chaque réponse")
    print("  ✅ Température baissée à 0.2 (plus déterministe)")
    print("  ✅ Instructions de fallback si aucun outil applicable")
    print()

    changes = fix_agent_hallucination()

    print("Changements appliqués:")
    for change in changes:
        print(f"  {change}")

    if not changes:
        print("  ⚠️  Aucun changement nécessaire")

    print()
    print("=" * 80)
    print("✅ FIX APPLIQUÉ - L'agent devrait maintenant TOUJOURS utiliser les tools")
    print("=" * 80)
    print()
    print("Note: Si l'agent hallucine toujours après ce fix,")
    print("il faudra utiliser tool_choice='required' dans l'API Anthropic")
    print("(nécessite modification du node n8n LangChain)")

if __name__ == "__main__":
    main()