import json

def create_lsp_response():
    response = {
        "jsonrpc": "2.0",
        "id": 104,
        "result": {
            "uri": "file:///frontend/src/app/api/agent/route.ts",
            "range": {
                "start": {"line": 15, "character": 4},
                "end": {"line": 25, "character": 5}
            },
            "metadata": {
                "node_type": "conditional_branch",
                "identifier": "ptst_specialist_mock",
                "cognitive_complexity_score": 14,
                "symbol_references": [
                    "file:///The Paraconsistent Twist-Structured Transformer (PTST).md:12"
                ]
            }
        }
    }
    with open('lsp_response.json', 'w', encoding='utf-8') as f:
        json.dump(response, f, indent=2)

if __name__ == "__main__":
    create_lsp_response()
