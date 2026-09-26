"""
Session 14 - Task 1: Basic MCP Server
======================================
This script starts a basic Model Context Protocol (MCP) server locally.
It listens over HTTP and responds with a static message whenever any
JSON-RPC request is received.

MCP uses JSON-RPC 2.0 as its underlying wire protocol.
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys

HOST = "127.0.0.1"
PORT = 8000

STATIC_RESPONSE_MESSAGE = (
    "Hello from MCP Server! Connection established successfully. "
    "This is a static response responding to your request."
)

class BasicMCPHandler(BaseHTTPRequestHandler):
    """
    HTTP Request Handler that processes JSON-RPC 2.0 requests
    and responds with a static MCP confirmation message.
    """

    def do_POST(self):
        # 1. Read request body
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)

        # 2. Parse incoming JSON-RPC payload
        req_id = 1
        method_name = "unknown"
        params = {}
        try:
            request_json = json.loads(post_data.decode("utf-8"))
            req_id = request_json.get("id", 1)
            method_name = request_json.get("method", "unknown")
            params = request_json.get("params", {})
            print(f"\n[+] Received JSON-RPC Request:")
            print(f"    - ID:     {req_id}")
            print(f"    - Method: {method_name}")
            print(f"    - Params: {json.dumps(params)}")
        except Exception as e:
            print(f"[-] Could not parse JSON body: {e}")

        # 3. Formulate JSON-RPC 2.0 compliant static response
        response_payload = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "status": "success",
                "protocol": "mcp-jsonrpc-2.0",
                "server": "Basic-MCP-Server-Task1",
                "received_method": method_name,
                "message": STATIC_RESPONSE_MESSAGE
            }
        }

        # 4. Send HTTP headers & response
        response_bytes = json.dumps(response_payload, indent=2).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.end_headers()
        self.wfile.write(response_bytes)

        print(f"[+] Sent Static JSON-RPC Response to client (ID: {req_id})")

    def do_GET(self):
        """Health check endpoint."""
        health = {
            "status": "running",
            "server": "Basic-MCP-Server-Task1",
            "protocol": "MCP JSON-RPC 2.0 over HTTP"
        }
        res_bytes = json.dumps(health, indent=2).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(res_bytes)))
        self.end_headers()
        self.wfile.write(res_bytes)

    def log_message(self, format, *args):
        # Override to suppress default HTTP access logs for clean console
        sys.stderr.write(f"[HTTP] {self.address_string()} - {args[0]} {args[1]}\n")

def start_server():
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, BasicMCPHandler)
    print("=" * 65)
    print("     SESSION 14 - TASK 1: BASIC LOCAL MCP SERVER")
    print("=" * 65)
    print(f"[*] MCP Server running at: http://{HOST}:{PORT}/")
    print(f"[*] Transport: HTTP (JSON-RPC 2.0)")
    print(f"[*] Static Message configured:")
    print(f"    \"{STATIC_RESPONSE_MESSAGE}\"")
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
