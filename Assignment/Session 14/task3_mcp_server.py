"""
Session 14 - Task 3: MCP Server with 'get_song_recommendation'
=============================================================
This script modifies the MCP Server to recognize the 'get_song_recommendation'
method. When called, it returns a JSON object containing a trending song title,
artist, album, genre, year, and Spotify metadata (simulating a Spotify-style feature).
"""

import json
import random
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys

# Ensure safe UTF-8 output on Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

HOST = "127.0.0.1"
PORT = 8000

# Curated Spotify-style trending songs catalogue
TRENDING_SONGS = [
    {
        "title": "Blinding Lights",
        "artist": "The Weeknd",
        "album": "After Hours",
        "genre": "Synthwave / Pop",
        "release_year": 2020,
        "duration": "3:20",
        "trending_rank": 1,
        "spotify_id": "0VjIjW4GlUZAMYd2vXMi3b",
        "spotify_url": "https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b",
        "popularity_score": 96,
        "energy": "High"
    },
    {
        "title": "As It Was",
        "artist": "Harry Styles",
        "album": "Harry's House",
        "genre": "Indie Pop",
        "release_year": 2022,
        "duration": "2:47",
        "trending_rank": 2,
        "spotify_id": "4Dvkj6JhhA12EX05QKi792",
        "spotify_url": "https://open.spotify.com/track/4Dvkj6JhhA12EX05QKi792",
        "popularity_score": 93,
        "energy": "Medium"
    },
    {
        "title": "Flowers",
        "artist": "Miley Cyrus",
        "album": "Endless Summer Vacation",
        "genre": "Disco-Pop",
        "release_year": 2023,
        "duration": "3:20",
        "trending_rank": 3,
        "spotify_id": "0yLWrDD02D0NIZAc9QO59Y",
        "spotify_url": "https://open.spotify.com/track/0yLWrDD02D0NIZAc9QO59Y",
        "popularity_score": 91,
        "energy": "High"
    },
    {
        "title": "Espresso",
        "artist": "Sabrina Carpenter",
        "album": "Short n' Sweet",
        "genre": "Nu-Disco / Pop",
        "release_year": 2024,
        "duration": "2:55",
        "trending_rank": 4,
        "spotify_id": "2qSkXiYOKWJDCcdHgRI5Zb",
        "spotify_url": "https://open.spotify.com/track/2qSkXiYOKWJDCcdHgRI5Zb",
        "popularity_score": 98,
        "energy": "High"
    },
    {
        "title": "Starboy",
        "artist": "The Weeknd ft. Daft Punk",
        "album": "Starboy",
        "genre": "R&B / Electropop",
        "release_year": 2016,
        "duration": "3:50",
        "trending_rank": 5,
        "spotify_id": "7MXVkk9YM5FZ0wSlOiDC47",
        "spotify_url": "https://open.spotify.com/track/7MXVkk9YM5FZ0wSlOiDC47",
        "popularity_score": 94,
        "energy": "High"
    },
    {
        "title": "Cruel Summer",
        "artist": "Taylor Swift",
        "album": "Lover",
        "genre": "Synth-pop",
        "release_year": 2019,
        "duration": "2:58",
        "trending_rank": 6,
        "spotify_id": "1BxfuPKGuaTgP7aM02wmWu",
        "spotify_url": "https://open.spotify.com/track/1BxfuPKGuaTgP7aM02wmWu",
        "popularity_score": 95,
        "energy": "High"
    },
    {
        "title": "Levitating",
        "artist": "Dua Lipa",
        "album": "Future Nostalgia",
        "genre": "Dance-Pop",
        "release_year": 2020,
        "duration": "3:23",
        "trending_rank": 7,
        "spotify_id": "463CkQjx2Zk1yXoBu1bsby",
        "spotify_url": "https://open.spotify.com/track/463CkQjx2Zk1yXoBu1bsby",
        "popularity_score": 90,
        "energy": "High"
    }
]

class SongRecommendationMCPHandler(BaseHTTPRequestHandler):
    """
    MCP Request Handler that processes JSON-RPC requests,
    identifying 'get_song_recommendation' method and returning
    a trending song object.
    """

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)

        req_id = 1
        method_name = ""
        params = {}

        try:
            request_json = json.loads(post_data.decode("utf-8"))
            req_id = request_json.get("id", 1)
            method_name = request_json.get("method", "")
            params = request_json.get("params", {})
        except Exception as e:
            self._send_error_response(req_id, -32700, f"Parse error: {e}")
            return

        print(f"\n[+] Incoming JSON-RPC Request:")
        print(f"    - ID:     {req_id}")
        print(f"    - Method: '{method_name}'")
        print(f"    - Params: {json.dumps(params)}")

        # Check if requested method is 'get_song_recommendation'
        if method_name == "get_song_recommendation":
            requested_genre = params.get("genre", "").lower()
            matching_songs = [
                s for s in TRENDING_SONGS
                if requested_genre in s["genre"].lower()
            ] if requested_genre else TRENDING_SONGS

            chosen_song = random.choice(matching_songs if matching_songs else TRENDING_SONGS)

            response_payload = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "status": "success",
                    "feature": "Spotify Trending Song Recommendation",
                    "recommendation": chosen_song
                }
            }
            print(f"[+] Method matched! Recommended: \"{chosen_song['title']}\" by {chosen_song['artist']}")

        elif method_name == "tools/list":
            # Standard MCP tool discovery
            response_payload = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": [
                        {
                            "name": "get_song_recommendation",
                            "description": "Returns a random trending song recommendation (Spotify-style)",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "genre": {"type": "string", "description": "Optional genre filter"}
                                }
                            }
                        }
                    ]
                }
            }
        else:
            # Fallback response for other methods
            response_payload = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "status": "success",
                    "server": "Spotify-MCP-Server-Task3",
                    "message": f"Method '{method_name}' acknowledged. Send 'get_song_recommendation' for trending music."
                }
            }

        self._send_json_response(response_payload)

    def _send_json_response(self, payload):
        response_bytes = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.end_headers()
        self.wfile.write(response_bytes)

    def _send_error_response(self, req_id, code, message):
        error_payload = {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": code, "message": message}
        }
        self._send_json_response(error_payload)

    def log_message(self, format, *args):
        sys.stderr.write(f"[HTTP] {self.address_string()} - {args[0]} {args[1]}\n")

def start_server():
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, SongRecommendationMCPHandler)
    print("=" * 65)
    print("     SESSION 14 - TASK 3: SPOTIFY-STYLE MCP SERVER")
    print("=" * 65)
    print(f"[*] MCP Server running at: http://{HOST}:{PORT}/")
    print(f"[*] Supported Method:     'get_song_recommendation'")
    print(f"[*] Available Songs:      {len(TRENDING_SONGS)} trending tracks in library")
    print("[*] Ready to accept incoming MCP requests...")
    print("[*] Press Ctrl+C to terminate.")
    print("=" * 65)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Shutting down MCP Server.")
        httpd.server_close()

if __name__ == "__main__":
    start_server()
