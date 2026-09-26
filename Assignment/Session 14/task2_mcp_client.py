"""
Session 14 - Task 2: Simple MCP Client
=======================================
This script creates a simple MCP client that sends a JSON-RPC request
to the local MCP Server using HTTP transport and prints the response
in the console.

Uses the Python 'requests' library to transmit the JSON-RPC payload.
"""

import json
import sys
import requests

SERVER_URL = "http://127.0.0.1:8000/"

def run_mcp_client():
    print("=" * 65)
    print("     SESSION 14 - TASK 2: SIMPLE MCP CLIENT (HTTP)")
    print("=" * 65)

    # 1. Prepare JSON-RPC 2.0 payload
    payload = {
        "jsonrpc": "2.0",
        "id": "client-req-001",
        "method": "initialize",
        "params": {
            "client_name": "Antigravity-MCP-Client",
            "protocol_version": "2024-11-05",
            "capabilities": {
                "roots": {"listChanged": True},
                "sampling": {}
            }
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    print(f"[*] Target Server URL: {SERVER_URL}")
    print(f"[*] Transport:         HTTP POST")
    print(f"[*] Sending JSON-RPC Request:")
    print(json.dumps(payload, indent=4))
    print("-" * 65)

    # 2. Send the HTTP POST request using 'requests'
    try:
        response = requests.post(SERVER_URL, json=payload, headers=headers, timeout=5)
        
        print(f"[*] HTTP Status Code:   {response.status_code} {response.reason}")
        print(f"[*] Response Headers:   {dict(response.headers)}")
        print("-" * 65)
        print("[*] Full JSON-RPC Response:")

        response_data = response.json()
        print(json.dumps(response_data, indent=4))
        print("-" * 65)

        # 3. Extract and display specific static message
        result = response_data.get("result", {})
        message = result.get("message", "No message received")
        print("[*] Extracted Static Server Message:")
        print(f"    >>> \"{message}\"")
        print("=" * 65)
        print("[SUCCESS] MCP Client received and validated server response!")

    except requests.exceptions.ConnectionError:
        print(f"[-] Connection Error: Could not connect to MCP Server at {SERVER_URL}.")
        print("    Please ensure 'task1_mcp_server.py' is running in another terminal.")
        sys.exit(1)
    except Exception as e:
        print(f"[-] An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_mcp_client()
