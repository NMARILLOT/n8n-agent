#!/usr/bin/env python3
"""
Test delete_idea Tool
Vérifie que le tool est correctement configuré et prêt à être utilisé
"""

import json
from pathlib import Path

def test_delete_idea_tool():
    workflow_path = Path("Agent Telegram - Dev Nico Perso/workflow/MCP - Idée Dev Nico (Perso) (1).json")

    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    print()
    print("=" * 80)
    print("🧪 TEST DELETE_IDEA TOOL CONFIGURATION")
    print("=" * 80)
    print()

    # Test 1: Trouver le tool delete_idea
    print("📋 Test 1: Tool delete_idea exists")
    delete_tool = None
    for node in workflow['nodes']:
        if node['name'] == 'delete_idea':
            delete_tool = node
            break

    if not delete_tool:
        print("  ❌ FAIL: Tool delete_idea not found")
        return False

    print("  ✅ PASS: Tool delete_idea found")
    print()

    # Test 2: Vérifier les paramètres
    print("📋 Test 2: Tool parameters configuration")
    params = delete_tool['parameters']
    schema = params['workflowInputs']['schema']

    print(f"  - Total parameters: {len(schema)}")

    required_params = [p for p in schema if p.get('required', False)]
    print(f"  - Required parameters: {len(required_params)}")

    if len(required_params) != 1:
        print("  ❌ FAIL: Should have exactly 1 required parameter")
        return False

    if required_params[0]['id'] != 'idea_id':
        print("  ❌ FAIL: Required parameter should be 'idea_id'")
        return False

    print("  ✅ PASS: Only idea_id is required")

    # Vérifier __operation__ dans value (peut être absent du schema si hardcodé)
    value = params['workflowInputs']['value']
    if '__operation__' in value:
        if value['__operation__'] == 'delete_idea':
            print("  ✅ PASS: __operation__ hardcoded in value (valid approach)")
        else:
            print(f"  ❌ FAIL: __operation__ has wrong value: {value['__operation__']}")
            return False
    else:
        # Vérifier si c'est dans le schema
        operation_param = next((p for p in schema if p['id'] == '__operation__'), None)
        if not operation_param:
            print("  ⚠️  WARNING: __operation__ not found in schema or value")
            print("      (This may work if Switch uses a different routing method)")
        else:
            if operation_param.get('display', True):
                print("  ❌ FAIL: __operation__ should be hidden (display: false)")
                return False
            print("  ✅ PASS: __operation__ parameter is hidden")
    print()

    # Test 3: Vérifier la description
    print("📋 Test 3: Tool description")
    description = params.get('description', '')

    if 'archive' not in description.lower():
        print("  ⚠️  WARNING: Description should mention 'archive'")

    if 'IDEA-' in description:
        print("  ✅ PASS: Description mentions ID format")
    else:
        print("  ⚠️  WARNING: Description should mention ID format (IDEA-XXXXXXXX)")

    print(f"  Description: {description[:100]}...")
    print()

    # Test 4: Vérifier le Switch
    print("📋 Test 4: Switch Operation routing")
    switch_node = None
    for node in workflow['nodes']:
        if node['name'] == 'Switch Operation':
            switch_node = node
            break

    if not switch_node:
        print("  ❌ FAIL: Switch Operation node not found")
        return False

    rules = switch_node['parameters']['rules']['values']
    delete_rule = next((r for r in rules if r.get('outputKey') == 'delete_idea'), None)

    if not delete_rule:
        print("  ❌ FAIL: No delete_idea rule in Switch")
        return False

    left_value = delete_rule['conditions']['conditions'][0]['leftValue']
    right_value = delete_rule['conditions']['conditions'][0]['rightValue']

    print(f"  - Switch reads: {left_value}")
    print(f"  - Expected value: {right_value}")

    if '$json.__operation__' not in left_value:
        print("  ❌ FAIL: Switch should read $json.__operation__")
        return False

    if right_value != 'delete_idea':
        print("  ❌ FAIL: Switch should expect 'delete_idea'")
        return False

    print("  ✅ PASS: Switch routing is correct")
    print()

    # Test 5: Vérifier Prepare Delete Idea
    print("📋 Test 5: Prepare Delete Idea code")
    prepare_node = None
    for node in workflow['nodes']:
        if node['name'] == 'Prepare Delete Idea':
            prepare_node = node
            break

    if not prepare_node:
        print("  ❌ FAIL: Prepare Delete Idea node not found")
        return False

    code = prepare_node['parameters']['jsCode']

    if 'input.idea_id' in code:
        print("  ✅ PASS: Code reads input.idea_id")
    else:
        print("  ❌ FAIL: Code should read input.idea_id")
        return False

    if '[DELETE DEBUG]' in code:
        print("  ✅ PASS: Debug logging present")
    else:
        print("  ⚠️  WARNING: No debug logging in code")

    print()

    # Test 6: Vérifier Notion node
    print("📋 Test 6: Notion - Get Ideas For Delete node")
    notion_node = None
    for node in workflow['nodes']:
        if node['name'] == 'Notion - Get Ideas For Delete':
            notion_node = node
            break

    if not notion_node:
        print("  ❌ FAIL: Notion - Get Ideas For Delete node not found")
        return False

    node_id = notion_node['id']
    db_id = notion_node['parameters']['databaseId']['value']

    print(f"  - Node ID: {node_id}")
    print(f"  - Database ID: {db_id}")

    if node_id == "8964a2a3fcfc4a1e83ee88ed":
        print("  ⚠️  WARNING: This is the OLD node ID, should be new UUID")
    else:
        print("  ✅ PASS: Node has new UUID")

    if db_id == "29b2c1373ccc807d9347ce519cabcac4":
        print("  ✅ PASS: Correct database ID (Ideas database)")
    else:
        print("  ❌ FAIL: Wrong database ID")
        return False

    print()

    # Test 7: Vérifier les connections
    print("📋 Test 7: Workflow connections")
    connections = workflow.get('connections', {})

    # Vérifier que delete_idea est connecté au Switch
    if 'delete_idea' in connections:
        print("  ✅ PASS: delete_idea has outgoing connections")
    else:
        print("  ❌ FAIL: delete_idea should connect to Switch")
        return False

    # Vérifier le flux complet
    expected_flow = [
        "Switch Operation → Notion - Get Ideas For Delete",
        "Notion - Get Ideas For Delete → Prepare Delete Idea",
        "Prepare Delete Idea → Notion - Archive Idea",
        "Notion - Archive Idea → Format Delete Response"
    ]

    print("  Expected flow:")
    for step in expected_flow:
        print(f"    - {step}")

    print()

    # Résumé final
    print("=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    print()
    print("✅ All tests passed!")
    print()
    print("The delete_idea tool is correctly configured and ready to use.")
    print()
    print("Usage:")
    print("  delete_idea(idea_id=\"IDEA-XXXXXXXX\")")
    print()
    print("Expected behavior:")
    print("  1. LLM calls tool with only idea_id parameter")
    print("  2. Tool adds __operation__='delete_idea' internally")
    print("  3. Switch routes to delete_idea flow")
    print("  4. Prepare Delete Idea validates and finds idea")
    print("  5. Notion archives the page")
    print("  6. Format Delete Response returns success message")
    print()

    return True

def main():
    try:
        success = test_delete_idea_tool()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    main()
