#!/usr/bin/env python3
"""
WORKFLOW PREVIEW - Visualisation locale des layouts n8n
Génère un HTML pour voir le layout AVANT de déployer
"""

import json
from pathlib import Path
import webbrowser
import http.server
import socketserver
import threading

def generate_html_preview(workflow_path):
    """Génère un HTML pour visualiser le workflow"""

    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    # Trouver les limites pour le viewport
    min_x = min_y = 10000
    max_x = max_y = -10000

    for node in workflow['nodes']:
        x, y = node['position']
        min_x = min(min_x, x)
        min_y = min(min_y, y)

        # Estimer la taille du node
        width = 200
        height = 100
        if node['type'] == 'n8n-nodes-base.stickyNote':
            width = node['parameters'].get('width', 400)
            height = node['parameters'].get('height', 300)

        max_x = max(max_x, x + width)
        max_y = max(max_y, y + height)

    # Ajouter du padding
    padding = 100
    viewport_width = max_x - min_x + padding * 2
    viewport_height = max_y - min_y + padding * 2

    # Couleurs n8n
    colors = {
        1: '#FFE5B4',  # Jaune pâle
        2: '#FFE4E1',  # Rose pâle
        3: '#FFB6C1',  # Rose
        4: '#E6F3FF',  # Bleu pâle
        5: '#F0E6FF',  # Violet pâle
        6: '#E6FFE6',  # Vert pâle
        7: '#FFE6CC',  # Orange pâle
    }

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{workflow_path.name} - Preview</title>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #2a2a2a;
            color: white;
        }}
        .container {{
            position: relative;
            width: {viewport_width}px;
            height: {viewport_height}px;
            background: #1a1a1a;
            border: 2px solid #444;
            margin: 20px auto;
            overflow: auto;
        }}
        .node {{
            position: absolute;
            background: #3a3a3a;
            border: 2px solid #666;
            border-radius: 8px;
            padding: 10px;
            font-size: 12px;
            color: white;
            min-width: 180px;
            min-height: 80px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
            z-index: 10;
        }}
        .sticky {{
            position: absolute;
            border-radius: 8px;
            padding: 15px;
            font-size: 13px;
            opacity: 0.9;
            z-index: 1;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }}
        .sticky h2 {{
            margin: 0 0 10px 0;
            font-size: 16px;
        }}
        .sticky ul {{
            margin: 5px 0;
            padding-left: 20px;
        }}
        .mcp-tool {{
            background: #2e5090;
            border-color: #4a6fa8;
        }}
        .trigger {{
            background: #8e44ad;
            border-color: #a569bd;
        }}
        .switch {{
            background: #e67e22;
            border-color: #f39c12;
        }}
        .notion {{
            background: #2c3e50;
            border-color: #34495e;
        }}
        .code {{
            background: #27ae60;
            border-color: #2ecc71;
        }}
        .ai-agent {{
            background: #c0392b;
            border-color: #e74c3c;
        }}
        .header {{
            padding: 20px;
            background: #1a1a1a;
            border-bottom: 1px solid #444;
        }}
        h1 {{
            margin: 0 0 10px 0;
        }}
        .stats {{
            color: #aaa;
            font-size: 14px;
        }}
        .controls {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: #2a2a2a;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #444;
            z-index: 1000;
        }}
        .controls button {{
            display: block;
            width: 100%;
            margin: 5px 0;
            padding: 8px;
            background: #3a3a3a;
            color: white;
            border: 1px solid #555;
            border-radius: 4px;
            cursor: pointer;
        }}
        .controls button:hover {{
            background: #4a4a4a;
        }}
        .connection {{
            stroke: #666;
            stroke-width: 2;
            fill: none;
            opacity: 0.5;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎨 {workflow_path.stem}</h1>
        <div class="stats">
            📦 {len([n for n in workflow['nodes'] if n['type'] != 'n8n-nodes-base.stickyNote'])} nodes •
            📌 {len([n for n in workflow['nodes'] if n['type'] == 'n8n-nodes-base.stickyNote'])} sticky notes •
            📐 Viewport: {viewport_width}x{viewport_height}px
        </div>
    </div>

    <div class="controls">
        <h3>🎮 Controls</h3>
        <button onclick="location.reload()">🔄 Refresh</button>
        <button onclick="zoomIn()">🔍 Zoom In</button>
        <button onclick="zoomOut()">🔍 Zoom Out</button>
        <button onclick="resetZoom()">↺ Reset</button>
    </div>

    <div class="container" id="container">
        <svg style="position: absolute; width: 100%; height: 100%; z-index: 0;">
"""

    # Dessiner les connexions (simplifié)
    if 'connections' in workflow:
        for source_name, connections in workflow.get('connections', {}).items():
            # Trouver le node source
            source_node = None
            for node in workflow['nodes']:
                if node['name'] == source_name:
                    source_node = node
                    break

            if source_node and 'main' in connections:
                sx, sy = source_node['position']
                sx = sx - min_x + padding + 100  # Centre du node
                sy = sy - min_y + padding + 50

                for outputs in connections.get('main', []):
                    if outputs:
                        for output in outputs:
                            target_name = output.get('node')
                            # Trouver le node cible
                            for node in workflow['nodes']:
                                if node['name'] == target_name:
                                    tx, ty = node['position']
                                    tx = tx - min_x + padding + 100
                                    ty = ty - min_y + padding + 50
                                    html += f'<line x1="{sx}" y1="{sy}" x2="{tx}" y2="{ty}" class="connection"/>\n'
                                    break

    html += "</svg>\n"

    # Générer les sticky notes
    for node in workflow['nodes']:
        if node['type'] == 'n8n-nodes-base.stickyNote':
            x, y = node['position']
            x = x - min_x + padding
            y = y - min_y + padding

            width = node['parameters'].get('width', 400)
            height = node['parameters'].get('height', 300)
            color = colors.get(node['parameters'].get('color', 4), '#E6F3FF')
            content = node['parameters'].get('content', '').replace('\n', '<br>')

            html += f"""
        <div class="sticky" style="left: {x}px; top: {y}px; width: {width}px; height: {height}px; background: {color}; color: #333;">
            {content}
        </div>
"""

    # Générer les nodes
    for node in workflow['nodes']:
        if node['type'] != 'n8n-nodes-base.stickyNote':
            x, y = node['position']
            x = x - min_x + padding
            y = y - min_y + padding

            # Déterminer la classe CSS
            css_class = 'node'
            if 'trigger' in node['name'].lower():
                css_class += ' trigger'
            elif 'switch' in node['name'].lower():
                css_class += ' switch'
            elif 'notion' in node['name'].lower():
                css_class += ' notion'
            elif 'code' in node['type'] or 'format' in node['name'].lower():
                css_class += ' code'
            elif 'agent' in node['name'].lower() or 'claude' in node['name'].lower():
                css_class += ' ai-agent'
            elif any(tool in node['name'].lower() for tool in ['search', 'get', 'create', 'update', 'delete', 'list']):
                css_class += ' mcp-tool'

            html += f"""
        <div class="{css_class}" style="left: {x}px; top: {y}px;">
            {node['name']}
        </div>
"""

    html += """
    </div>

    <script>
        let scale = 1;
        const container = document.getElementById('container');

        function zoomIn() {
            scale += 0.1;
            container.style.transform = `scale(${scale})`;
            container.style.transformOrigin = 'top left';
        }

        function zoomOut() {
            scale = Math.max(0.5, scale - 0.1);
            container.style.transform = `scale(${scale})`;
            container.style.transformOrigin = 'top left';
        }

        function resetZoom() {
            scale = 1;
            container.style.transform = `scale(${scale})`;
        }

        // Drag to pan
        let isDragging = false;
        let startX, startY, scrollLeft, scrollTop;

        container.addEventListener('mousedown', (e) => {
            isDragging = true;
            startX = e.pageX - container.offsetLeft;
            startY = e.pageY - container.offsetTop;
            scrollLeft = container.scrollLeft;
            scrollTop = container.scrollTop;
            container.style.cursor = 'grabbing';
        });

        container.addEventListener('mouseup', () => {
            isDragging = false;
            container.style.cursor = 'grab';
        });

        container.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            e.preventDefault();
            const x = e.pageX - container.offsetLeft;
            const y = e.pageY - container.offsetTop;
            const walkX = (x - startX) * 2;
            const walkY = (y - startY) * 2;
            container.scrollLeft = scrollLeft - walkX;
            container.scrollTop = scrollTop - walkY;
        });

        container.style.cursor = 'grab';
    </script>
</body>
</html>"""

    return html

def serve_preview():
    """Lance un serveur HTTP local"""
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", 8888), Handler) as httpd:
        print("🌐 Serveur lancé sur http://localhost:8888")
        print("📌 Appuie sur Ctrl+C pour arrêter")
        httpd.serve_forever()

def main():
    print("=" * 60)
    print("🎨 WORKFLOW PREVIEW - Visualisation locale")
    print("=" * 60)

    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    # Générer les previews
    workflows = [
        project_root / "Agent Telegram - Dev Nico Perso" / "workflow" / "MCP - Idée Dev Nico (Perso) (1).json",
        project_root / "Agent Telegram - Dev Nico Perso" / "workflow" / "Agent Telegram - Dev Ideas.json"
    ]

    preview_dir = project_root / "preview"
    preview_dir.mkdir(exist_ok=True)

    print("\n📦 Génération des previews...")
    for workflow_path in workflows:
        if workflow_path.exists():
            html = generate_html_preview(workflow_path)
            preview_path = preview_dir / f"{workflow_path.stem}.html"
            with open(preview_path, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"  ✅ {workflow_path.stem}.html")

    # Créer un index
    index_html = """<!DOCTYPE html>
<html>
<head>
    <title>n8n Workflow Previews</title>
    <style>
        body {
            margin: 0;
            padding: 40px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #2a2a2a;
            color: white;
        }
        h1 {
            margin-bottom: 30px;
        }
        .workflow-card {
            background: #1a1a1a;
            border: 2px solid #444;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            display: block;
            text-decoration: none;
            color: white;
            transition: all 0.3s;
        }
        .workflow-card:hover {
            background: #2a2a2a;
            border-color: #666;
            transform: translateX(5px);
        }
        .workflow-title {
            font-size: 20px;
            margin-bottom: 10px;
        }
        .workflow-desc {
            color: #aaa;
        }
    </style>
</head>
<body>
    <h1>🎨 n8n Workflow Previews</h1>

    <a href="MCP - Idée Dev Nico (Perso) (1).html" class="workflow-card">
        <div class="workflow-title">📦 MCP - Idée Dev Nico (Perso)</div>
        <div class="workflow-desc">Serveur MCP pour gestion des projets et idées</div>
    </a>

    <a href="Agent Telegram - Dev Ideas.html" class="workflow-card">
        <div class="workflow-title">🤖 Agent Telegram - Dev Ideas</div>
        <div class="workflow-desc">Agent Telegram pour capturer les idées</div>
    </a>
</body>
</html>"""

    with open(preview_dir / "index.html", 'w', encoding='utf-8') as f:
        f.write(index_html)

    print("\n🌐 Ouverture dans le navigateur...")
    webbrowser.open(f"file://{preview_dir / 'index.html'}")

    print("\n" + "=" * 60)
    print("✨ Preview disponible dans ton navigateur!")
    print("   Tu peux voir et ajuster les layouts")
    print("   Actualise la page après chaque modification")
    print("=" * 60)

if __name__ == "__main__":
    main()