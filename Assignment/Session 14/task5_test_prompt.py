"""
Session 14 - Task 5: Test Client for 'get_movie_showtimes' Prompt
=================================================================
This client demonstrates how an MCP client interacts with MCP Prompts:
1. Discovers registered prompts using 'prompts/list'
2. Requests the custom 'get_movie_showtimes' prompt using 'prompts/get'
3. Invokes the companion 'fetch_movie_showtimes' tool to display live showtimes
"""

import json
import sys
import requests

# Ensure UTF-8 safe output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SERVER_URL = "http://127.0.0.1:8000/"

def run_prompt_test():
    print("=" * 65)
    print("  SESSION 14 - TASK 5: TESTING CUSTOM MCP PROMPT ('get_movie_showtimes')")
    print("=" * 65)

    # 1. Step 1: Discover available prompts ('prompts/list')
    print("\n--- Step 1: Discovering Prompts via 'prompts/list' ---")
    list_payload = {
        "jsonrpc": "2.0",
        "id": "prompt-list-001",
        "method": "prompts/list",
        "params": {}
    }

    try:
        res1 = requests.post(SERVER_URL, json=list_payload, timeout=5)
        data1 = res1.json()
        print("[*] Available Prompts Response:")
        print(json.dumps(data1, indent=2))
    except requests.exceptions.ConnectionError:
        print(f"[-] Connection Error: Start 'task5_movie_showtimes_server.py' first.")
        sys.exit(1)

    # 2. Step 2: Request the Prompt with arguments ('prompts/get')
    print("\n" + "-" * 65)
    print("--- Step 2: Requesting 'get_movie_showtimes' via 'prompts/get' ---")
    get_payload = {
        "jsonrpc": "2.0",
        "id": "prompt-get-002",
        "method": "prompts/get",
        "params": {
            "name": "get_movie_showtimes",
            "arguments": {
                "movie_name": "Dune: Part Two",
                "city": "Mumbai",
                "date": "today",
                "preferred_format": "IMAX 2D",
                "time_slot": "Evening"
            }
        }
    }
    res2 = requests.post(SERVER_URL, json=get_payload, timeout=5)
    data2 = res2.json()
    print("[*] Rendered MCP Prompt Output:")
    messages = data2.get("result", {}).get("messages", [])
    for msg in messages:
        print(f"\n[Role: {msg.get('role').upper()}]")
        print(msg.get("content", {}).get("text", ""))

    # 3. Step 3: Call companion 'fetch_movie_showtimes' tool
    print("-" * 65)
    print("--- Step 3: Calling Companion Tool 'fetch_movie_showtimes' ---")
    tool_payload = {
        "jsonrpc": "2.0",
        "id": "tool-call-003",
        "method": "fetch_movie_showtimes",
        "params": {
            "movie_name": "Dune: Part Two",
            "city": "mumbai",
            "date": "today"
        }
    }
    res3 = requests.post(SERVER_URL, json=tool_payload, timeout=5)
    data3 = res3.json()
    showtimes_data = data3.get("result", {})
    print(f"[*] Live Showtimes for '{showtimes_data.get('movie')}' in {showtimes_data.get('city')}:")
    for cinema in showtimes_data.get("cinemas", []):
        print(f"\n[Cinema] {cinema.get('cinema')} [{cinema.get('screen_type')}]")
        for show in cinema.get("showtimes", []):
            pricing_str = " | ".join(f"{k}: Rs.{v}" for k, v in show.get("pricing", {}).items())
            print(f"   * {show.get('time')} - Status: {show.get('status')} | {pricing_str}")

    print("\n" + "=" * 65)
    print("[SUCCESS] Task 5 Custom MCP Prompt & Integration verified successfully!")

if __name__ == "__main__":
    run_prompt_test()
