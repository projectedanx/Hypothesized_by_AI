import os
import json
import re

def build_index():
    index = {"jsonrpc": "2.0", "result": {"nodes": [], "edges": []}, "id": 1}

    files = [f for f in os.listdir('.') if f.endswith('.md')]
    for f in files:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            # Extract headers
            headers = re.findall(r'^(#+)\s+(.*)', content, re.MULTILINE)
            for level, title in headers:
                index["result"]["nodes"].append({
                    "node_type": "heading",
                    "identifier": title.strip(),
                    "location": {"uri": f"file:///{f}"}
                })

    with open('semantic_index.json', 'w', encoding='utf-8') as out:
        json.dump(index, out, indent=2)

if __name__ == "__main__":
    build_index()
