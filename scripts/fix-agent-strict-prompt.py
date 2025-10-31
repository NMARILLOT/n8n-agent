#!/usr/bin/env python3
"""
Fix Agent System Prompt - Version ULTRA STRICTE
Problème: L'agent hallucine des succès sans appeler les tools
Solution: Prompt beaucoup plus agressif avec checklist de validation
"""

import json
from pathlib import Path

def fix_agent_prompt():
    workflow_path = Path("Agent Telegram - Dev Nico Perso/workflow/Agent Telegram - Dev Ideas.json")

    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    changes_made = []

    # Trouver le node Agent
    for node in workflow['nodes']:
        if node['type'] == '@n8n/n8n-nodes-langchain.agent':
            options = node['parameters']['options']

            # 1. BAISSER LA TEMPÉRATURE
            old_temp = options.get('temperature', 0.7)
            options['temperature'] = 0.2  # Beaucoup plus déterministe
            changes_made.append(f"✓ Température: {old_temp} → 0.2")

            # 2. AJOUTER UN PROMPT ULTRA STRICT AU DÉBUT
            current_prompt = options['systemMessage']

            ultra_strict_prefix = """🚨 RÈGLES CRITIQUES - JAMAIS DÉSOBÉIR 🚨

AVANT CHAQUE RÉPONSE, TU DOIS TE POSER CES QUESTIONS:

1. ❓ Est-ce une ACTION (créer/supprimer/modifier/chercher) ?
   → OUI ? Va à l'étape 2
   → NON ? Réponds directement (conversation simple)

2. ⚠️ AI-JE APPELÉ L'OUTIL CORRESPONDANT ?
   → OUI ? Continue à l'étape 3
   → NON ? ❌ STOP ! APPELLE L'OUTIL D'ABORD !

3. ✅ AI-JE REÇU UN RÉSULTAT DE L'OUTIL ?
   → OUI ? Tu peux confirmer avec les données reçues
   → NON ? ❌ NE CONFIRME RIEN ! Dis qu'il y a eu une erreur

🚫 INTERDICTIONS ABSOLUES:

- Tu ne peux PAS dire "✅ Supprimé" sans avoir appelé delete_idea()
- Tu ne peux PAS dire "✅ Créé" sans avoir appelé create_*()
- Tu ne peux PAS dire "✅ Modifié" sans avoir appelé update_*()
- Tu ne peux PAS inventer des IDs (IDEA-XXX, PROJ-XXX)

SI TU CONFIRMES UNE ACTION SANS AVOIR APPELÉ L'OUTIL:
→ Tu MENS à l'utilisateur
→ Tu crées de la CONFUSION
→ Tu détruis la CONFIANCE

CHECKLIST DE VALIDATION AVANT RÉPONSE:
□ C'est une action ? → Outil appelé ?
□ Outil a retourné un résultat ?
□ Je confirme SEULEMENT avec les données reçues ?

═══════════════════════════════════════════════════════════

"""

            new_prompt = ultra_strict_prefix + current_prompt
            options['systemMessage'] = new_prompt
            changes_made.append("✓ Ajouté checklist de validation au début du prompt")

            # 3. AJOUTER UN RAPPEL À LA FIN
            ultra_strict_suffix = """

═══════════════════════════════════════════════════════════

🔴 RAPPEL FINAL - LIS AVANT CHAQUE RÉPONSE:

Si l'utilisateur dit "supprime IDEA-123":
1. Appelle delete_idea("IDEA-123")
2. Attends le résultat
3. SI succès → Confirme avec les données reçues
4. SI échec → Dis qu'il y a eu une erreur

NE DIS JAMAIS "✅ Supprimé" AVANT D'AVOIR LE RÉSULTAT DE L'OUTIL !

C'est NON-NÉGOCIABLE. C'est ta responsabilité principale."""

            options['systemMessage'] = new_prompt + ultra_strict_suffix
            changes_made.append("✓ Ajouté rappel final de validation")

            break

    # Sauvegarder
    with open(workflow_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    return changes_made

def main():
    print()
    print("=" * 80)
    print("🚨 FIX AGENT HALLUCINATION - VERSION ULTRA STRICTE")
    print("=" * 80)
    print()
    print("Problème:")
    print("  L'agent dit '✅ Supprimé' sans appeler delete_idea()")
    print("  Il hallucine le succès au lieu d'utiliser les tools")
    print()
    print("Solution:")
    print("  1. Baisser température à 0.2 (très déterministe)")
    print("  2. Ajouter checklist de validation AVANT le prompt")
    print("  3. Ajouter rappel de validation APRÈS le prompt")
    print("  4. Rendre les règles plus agressives et visibles")
    print()

    changes = fix_agent_prompt()

    print("Changements:")
    for change in changes:
        print(f"  {change}")
    print()
    print("=" * 80)
    print("Le prompt inclut maintenant:")
    print("  🚨 Checklist de validation en HAUT")
    print("  🔴 Rappel final en BAS")
    print("  ⚠️ Température à 0.2 (au lieu de 0.7)")
    print()
    print("L'agent DOIT maintenant:")
    print("  1. Se poser les questions de validation")
    print("  2. Appeler l'outil AVANT de confirmer")
    print("  3. Confirmer SEULEMENT avec les données reçues")
    print("=" * 80)
    print()

if __name__ == "__main__":
    main()
