"""
Session 14 - Task 4: stdio MCP Server
======================================
This script runs an MCP Server using the 'stdio' transport mechanism.
It reads JSON-RPC 2.0 requests line-by-line from standard input (sys.stdin),
processes the request (including 'get_song_recommendation' and static fallback),
and writes JSON-RPC 2.0 responses to standard output (sys.stdout).

CRITICAL MCP STDIO RULE:
All diagnostic and debug messages MUST be written to sys.stderr so that
the JSON-RPC protocol stream on sys.stdout remains clean and uncorrupted.
"""

import sys
import json
import random

# Ensure UTF-8 safe stdio
if sys.platform == "win32":
    try:
        sys.stdin.reconfigure(encoding="utf-8")
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

TRENDING_SONGS = [
    {
        "title": "Blinding Lights",
        "artist": "The Weeknd",
        "album": "After Hours",
        "genre": "Synthwave / Pop",
        "release_year": 2020,
        "duration": "3:20",
        "trending_rank": 1,
        "spotify_url": "https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b"
    },
    {
        "title": "Espresso",
        "artist": "Sabrina Carpenter",
        "album": "Short n' Sweet",
        "genre": "Pop / Dance-Pop",
        "release_year": 2024,
        "duration": "2:55",
        "trending_rank": 2,
        "spotify_url": "https://open.spotify.com/track/2qSkXiYOKWJDCcdHgRI5Zb"
    },
    {
        "title": "Cruel Summer",
        "artist": "Taylor Swift",
        "album": "Lover",
        "genre": "Synth-pop",
        "release_year": 2019,
        "duration": "2:58",
        "trending_rank": 3,
        "spotify_url": "https://open.spotify.com/track/1BxfuPKGuaTgP7aM02wmWu"
    },
    {
        "title": "Starboy",
        "artist": "The Weeknd ft. Daft Punk",
        "album": "Starboy",
        "genre": "R&B / Electropop",
        "release_year": 2016,
        "duration": "3:50",
        "trending_rank": 4,
        "spotify_url": "https://open.spotify.com/track/7MXVkk9YM5FZ0wSlOiDC47"
    }
]

def log(msg):
    """Write log messages to stderr exclusively."""
    sys.stderr.write(f"[MCP-STDIO-SERVER] {msg}\n")
    sys.stderr.flush()

def handle_request(raw_line):
    raw_line = raw_line.strip()
    if not raw_line:
        return None

    try:
        req = json.loads(raw_line)
    except Exception as e:
        log(f"Failed to parse JSON: {e}")
        return {
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32700, "message": f"Parse error: {e}"}
        }

    req_id = req.get("id")
    method = req.get("method", "")
    params = req.get("params", {})
    log(f"Processing method='{method}' with id={req_id}")

    if method == "get_song_recommendation":
        chosen_song = random.choice(TRENDING_SONGS)
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "status": "success",
                "transport": "stdio",
                "recommendation": chosen_song
            }
        }
    elif method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {"listChanged": False}
                },
                "serverInfo": {
                    "name": "stdio-mcp-server",
                    "version": "1.0.0"
                }
            }
        }
    else:
        # Fallback static response
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "status": "success",
                "transport": "stdio",
                "server": "stdio-mcp-server",
                "message": f"Static message from stdio server. Method '{method}' handled."
            }
        }

def run_stdio_server():
    log("Server initialized. Waiting for JSON-RPC messages on stdin...")
    for line in sys.stdin:
        response = handle_request(line)
        if response is not None:
            # Must write single-line JSON followed by newline to stdout
            out_str = json.dumps(response)
            sys.stdout.write(out_str + "\n")
            sys.stdout.flush()
            log(f"Sent response for id={response.get('id')}")

if __name__ == "__main__":
    run_stdio_server()
