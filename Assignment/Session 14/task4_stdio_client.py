"""
Session 14 - Task 4: stdio MCP Client
======================================
This script updates the MCP Client to use the 'stdio' transport instead
of HTTP. It spawns the MCP Server as a local subprocess and communicates
bidirectionally by writing JSON-RPC requests to the server's stdin and
reading JSON-RPC responses from the server's stdout.
"""

import sys
import os
import json
import subprocess

# Ensure UTF-8 safe output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def run_stdio_client():
    print("=" * 65)
    print("    SESSION 14 - TASK 4: MCP CLIENT (stdio TRANSPORT)")
    print("=" * 65)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    server_script = os.path.join(current_dir, "task4_stdio_server.py")

    print(f"[*] Transport:             stdio (Standard Input/Output Pipes)")
    print(f"[*] Spawning MCP Server:   {server_script}")

    # Launch server subprocess with pipes for stdin, stdout, and stderr
    proc = subprocess.Popen(
        [sys.executable, "-u", server_script],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        bufsize=1
    )

    try:
        # 1. Send Request 1: Static message / initialize
        print("\n--- Step 1: Sending 'initialize' JSON-RPC Request via stdio ---")
        init_request = {
            "jsonrpc": "2.0",
            "id": "stdio-req-001",
            "method": "initialize",
            "params": {"clientInfo": {"name": "AntigravityStdioClient", "version": "1.0"}}
        }
        print("[*] Sent to stdin:")
        print(json.dumps(init_request, indent=2))

        # Write request line and flush
        proc.stdin.write(json.dumps(init_request) + "\n")
        proc.stdin.flush()

        # Read response from server stdout
        init_response_raw = proc.stdout.readline()
        init_response = json.loads(init_response_raw.strip())
        print("[*] Received from stdout:")
        print(json.dumps(init_response, indent=2))

        # 2. Send Request 2: 'get_song_recommendation' method
        print("\n--- Step 2: Sending 'get_song_recommendation' via stdio ---")
        song_request = {
            "jsonrpc": "2.0",
            "id": "stdio-req-002",
            "method": "get_song_recommendation",
            "params": {}
        }
        print("[*] Sent to stdin:")
        print(json.dumps(song_request, indent=2))

        proc.stdin.write(json.dumps(song_request) + "\n")
        proc.stdin.flush()

        song_response_raw = proc.stdout.readline()
        song_response = json.loads(song_response_raw.strip())
        print("[*] Received from stdout:")
        print(json.dumps(song_response, indent=2))

        song = song_response.get("result", {}).get("recommendation", {})
        if song:
            print("\n[+] Song Received over stdio Pipe:")
            print(f"    * Title:  {song.get('title')}")
            print(f"    * Artist: {song.get('artist')}")
            print(f"    * Genre:  {song.get('genre')}")
            print(f"    * URL:    {song.get('spotify_url')}")

        print("\n" + "=" * 65)
        print("[SUCCESS] stdio transport communication completed flawlessly!")

    finally:
        # Cleanly shut down subprocess
        proc.stdin.close()
        proc.terminate()
        proc.wait(timeout=3)
        print("[*] Server child process terminated cleanly.")

if __name__ == "__main__":
    run_stdio_client()
