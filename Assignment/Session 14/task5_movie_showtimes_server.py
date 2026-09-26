"""
Session 14 - Task 5: MCP Server with BookMyShow 'get_movie_showtimes' Prompt & Tool
===================================================================================
This script implements an MCP Server with:
1. Custom Prompt: 'get_movie_showtimes' (BookMyShow-style assistant prompt)
2. Prompt Discovery ('prompts/list') and Resolution ('prompts/get')
3. Companion Tool: 'fetch_movie_showtimes' with cinema halls, formats, and pricing
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys

# Ensure UTF-8 safe console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

HOST = "127.0.0.1"
PORT = 8000

# Mock BookMyShow Database
CINEMA_SHOWTIMES_DB = {
    "mumbai": [
        {
            "cinema": "PVR ICON: Phoenix Palladium, Lower Parel",
            "screen_type": "IMAX Laser 2D",
            "showtimes": [
                {"time": "01:30 PM", "status": "Available", "pricing": {"Classic": 450, "Prime": 650, "Recliner": 950}},
                {"time": "05:00 PM", "status": "Filling Fast", "pricing": {"Classic": 500, "Prime": 750, "Recliner": 1100}},
                {"time": "08:30 PM", "status": "Almost Full", "pricing": {"Classic": 550, "Prime": 850, "Recliner": 1250}}
            ]
        },
        {
            "cinema": "INOX Megaplex: Inorbit Mall, Malad",
            "screen_type": "MX4D / Dolby Atmos",
            "showtimes": [
                {"time": "02:15 PM", "status": "Available", "pricing": {"Silver": 320, "Gold": 480, "Club": 700}},
                {"time": "06:45 PM", "status": "Filling Fast", "pricing": {"Silver": 380, "Gold": 550, "Club": 850}}
            ]
        }
    ],
    "bengaluru": [
        {
            "cinema": "PVR Forum Mall: Koramangala",
            "screen_type": "IMAX with Laser",
            "showtimes": [
                {"time": "03:00 PM", "status": "Available", "pricing": {"Classic": 400, "Prime": 600, "Recliner": 900}},
                {"time": "07:30 PM", "status": "Filling Fast", "pricing": {"Classic": 450, "Prime": 700, "Recliner": 1050}}
            ]
        },
        {
            "cinema": "Cinepolis: Orion Mall, Rajajinagar",
            "screen_type": "4DX 3D",
            "showtimes": [
                {"time": "04:15 PM", "status": "Available", "pricing": {"Executive": 350, "VIP": 500, "Recliner": 750}}
            ]
        }
    ]
}

PROMPT_METADATA = {
    "name": "get_movie_showtimes",
    "description": "BookMyShow-style cinema assistant prompt to query live movie showtimes, cinema halls, formats (IMAX, 4DX, 2D), seat categories, and ticket pricing.",
    "arguments": [
        {"name": "movie_name", "description": "Title of the movie to query", "required": True},
        {"name": "city", "description": "City or locality (e.g. Mumbai, Bengaluru, Delhi-NCR)", "required": True},
        {"name": "date", "description": "Show date (default: 'today')", "required": False},
        {"name": "preferred_format", "description": "Format filter: IMAX 2D, 4DX, 2D, Any", "required": False},
        {"name": "time_slot", "description": "Preferred time slot (Morning, Afternoon, Evening, Night)", "required": False}
    ]
}

def generate_prompt_content(args):
    movie_name = args.get("movie_name", "Unknown Movie")
    city = args.get("city", "Mumbai")
    date = args.get("date", "today")
    fmt = args.get("preferred_format", "Any")
    slot = args.get("time_slot", "Any")

    instruction_text = f"""
You are a BookMyShow Cinema Concierge Assistant.

### USER QUERY CONTEXT:
- Movie Title:      {movie_name}
- City:             {city}
- Date:             {date}
- Preferred Format: {fmt}
- Preferred Slot:   {slot}

### INSTRUCTIONS:
1. Call the MCP tool 'fetch_movie_showtimes' with movie_name='{movie_name}', city='{city}', date='{date}'.
2. Group showtimes by Cinema Hall and display audio/visual formats (IMAX, 4DX, etc.).
3. Present seat categories with exact pricing in INR (₹) and seat availability status (🟢 Available, 🟡 Filling Fast, 🔴 Almost Full).
4. Highlight the best matching show according to preferred format '{fmt}' and slot '{slot}'.
5. Prompt the user to confirm ticket count and proceed to booking.
"""
    return [
        {
            "role": "user",
            "content": {
                "type": "text",
                "text": instruction_text.strip()
            }
        }
    ]

class MoviePromptMCPHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)

        req_id = 1
        method_name = ""
        params = {}

        try:
            req_json = json.loads(post_data.decode("utf-8"))
            req_id = req_json.get("id", 1)
            method_name = req_json.get("method", "")
            params = req_json.get("params", {})
        except Exception as e:
            self._send_response(req_id, error={"code": -32700, "message": str(e)})
            return

        print(f"\n[+] Request: method='{method_name}', id={req_id}")

        # 1. MCP Prompts List ('prompts/list')
        if method_name == "prompts/list":
            res = {"prompts": [PROMPT_METADATA]}
            self._send_response(req_id, result=res)

        # 2. MCP Prompts Get ('prompts/get')
        elif method_name == "prompts/get":
            prompt_name = params.get("name")
            prompt_args = params.get("arguments", {})
            if prompt_name == "get_movie_showtimes":
                messages = generate_prompt_content(prompt_args)
                res = {
                    "description": f"BookMyShow Prompt for {prompt_args.get('movie_name', 'Movie')}",
                    "messages": messages
                }
                self._send_response(req_id, result=res)
            else:
                self._send_response(req_id, error={"code": -32601, "message": f"Prompt '{prompt_name}' not found"})

        # 3. MCP Tools Call ('fetch_movie_showtimes' or 'tools/call')
        elif method_name in ("fetch_movie_showtimes", "tools/call"):
            args = params.get("arguments", params)
            city_key = args.get("city", "mumbai").lower()
            movie = args.get("movie_name", "Featured Movie")
            shows = CINEMA_SHOWTIMES_DB.get(city_key, CINEMA_SHOWTIMES_DB["mumbai"])
            res = {
                "movie": movie,
                "city": city_key.capitalize(),
                "date": args.get("date", "today"),
                "cinemas": shows
            }
            self._send_response(req_id, result=res)

        # 4. MCP Tools List ('tools/list')
        elif method_name == "tools/list":
            res = {
                "tools": [
                    {
                        "name": "fetch_movie_showtimes",
                        "description": "Fetch cinema halls, formats, showtimes, and ticket pricing",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "movie_name": {"type": "string"},
                                "city": {"type": "string"},
                                "date": {"type": "string"}
                            },
                            "required": ["movie_name", "city"]
                        }
                    }
                ]
            }
            self._send_response(req_id, result=res)

        # 5. Fallback
        else:
            self._send_response(req_id, result={
                "server": "BookMyShow-MCP-Server",
                "message": f"Acknowledged '{method_name}'. Query 'prompts/list' or 'prompts/get'."
            })

    def _send_response(self, req_id, result=None, error=None):
        payload = {"jsonrpc": "2.0", "id": req_id}
        if error:
            payload["error"] = error
        else:
            payload["result"] = result

        data = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format, *args):
        sys.stderr.write(f"[HTTP] {self.address_string()} - {args[0]} {args[1]}\n")

def start_server():
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, MoviePromptMCPHandler)
    print("=" * 65)
    print("     SESSION 14 - TASK 5: BOOKMYSHOW MCP PROMPT SERVER")
    print("=" * 65)
    print(f"[*] Server running at: http://{HOST}:{PORT}/")
    print(f"[*] Custom Prompt:     'get_movie_showtimes'")
    print(f"[*] Companion Tool:    'fetch_movie_showtimes'")
    print("[*] Ready for 'prompts/list', 'prompts/get', and 'tools/call'...")
    print("[*] Press Ctrl+C to stop.")
    print("=" * 65)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Shutting down server.")
        httpd.server_close()

if __name__ == "__main__":
    start_server()
