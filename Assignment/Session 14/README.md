# SESSION 14 – Introduction to Model Context Protocol (MCP)

This repository contains the complete implementation and solutions for all tasks under **Session 14: Introduction to MCP**.

---

## Overview of Tasks & Created Files

| Task | Topic | Files Created | Description |
| :--- | :--- | :--- | :--- |
| **Task 1** | MCP Package & Basic Server | [`task1_mcp_server.py`](file:///d:/tops%20data/Agentic%20AI/Assignment/Session%2014/task1_mcp_server.py) | Local MCP HTTP Server responding with a static message to any JSON-RPC request. |
| **Task 2** | MCP HTTP Client | [`task2_mcp_client.py`](file:///d:/tops%20data/Agentic%20AI/Assignment/Session%2014/task2_mcp_client.py) | Python client using `requests` sending JSON-RPC 2.0 payloads over HTTP transport. |
| **Task 3** | Trending Song Feature | [`task3_mcp_server.py`](file:///d:/tops%20data/Agentic%20AI/Assignment/Session%2014/task3_mcp_server.py)<br>[`task3_mcp_client.py`](file:///d:/tops%20data/Agentic%20AI/Assignment/Session%2014/task3_mcp_client.py) | Server modified to support `get_song_recommendation` returning Spotify-style metadata. |
| **Task 4** | stdio vs HTTP Transport | [`task4_transport_comparison.md`](file:///d:/tops%20data/Agentic%20AI/Assignment/Session%2014/task4_transport_comparison.md)<br>[`task4_stdio_server.py`](file:///d:/tops%20data/Agentic%20AI/Assignment/Session%2014/task4_stdio_server.py)<br>[`task4_stdio_client.py`](file:///d:/tops%20data/Agentic%20AI/Assignment/Session%2014/task4_stdio_client.py) | Technical comparison note + MCP Client & Server updated to use `stdio` pipes. |
| **Task 5** | Custom Movie Showtimes Prompt | [`task5_movie_showtimes.md`](file:///d:/tops%20data/Agentic%20AI/Assignment/Session%2014/task5_movie_showtimes.md)<br>[`task5_movie_showtimes_server.py`](file:///d:/tops%20data/Agentic%20AI/Assignment/Session%2014/task5_movie_showtimes_server.py)<br>[`task5_test_prompt.py`](file:///d:/tops%20data/Agentic%20AI/Assignment/Session%2014/task5_test_prompt.py) | Custom BookMyShow `get_movie_showtimes` MCP prompt with companion tool & integration. |

---

## Detailed Task Documentation & Execution

### Task 1: MCP Server with Static Response
- **Goal**: Start a basic MCP Server locally that responds with a static message when any request is received.
- **Protocol**: JSON-RPC 2.0 over HTTP (`http://127.0.0.1:8000/`).
- **To Run**:
  ```bash
  python task1_mcp_server.py
  ```

### Task 2: Simple MCP Client using `requests`
- **Goal**: Send a JSON-RPC request to the MCP Server using HTTP transport and print the response.
- **To Run**:
  ```bash
  # Terminal 1: Run the server
  python task1_mcp_server.py

  # Terminal 2: Run the client
  python task2_mcp_client.py
  ```
- **Sample Client Output**:
  ```text
  [*] HTTP Status Code: 200 OK
  [*] Full JSON-RPC Response:
  {
      "jsonrpc": "2.0",
      "id": "client-req-001",
      "result": {
          "status": "success",
          "protocol": "mcp-jsonrpc-2.0",
          "server": "Basic-MCP-Server-Task1",
          "received_method": "initialize",
          "message": "Hello from MCP Server! Connection established successfully. This is a static response responding to your request."
      }
  }
  ```

---

### Task 3: Spotify-Style Song Recommendation
- **Goal**: Recognize the `get_song_recommendation` method and return a random trending song object with Spotify metadata (title, artist, album, genre, release year, duration, Spotify URL, and trending rank).
- **To Run**:
  ```bash
  # Terminal 1: Run Task 3 server
  python task3_mcp_server.py

  # Terminal 2: Run Task 3 client
  python task3_mcp_client.py
  ```
- **Sample Response**:
  ```json
  {
    "jsonrpc": "2.0",
    "id": "req-song-001",
    "result": {
      "status": "success",
      "feature": "Spotify Trending Song Recommendation",
      "recommendation": {
        "title": "Blinding Lights",
        "artist": "The Weeknd",
        "album": "After Hours",
        "genre": "Synthwave / Pop",
        "release_year": 2020,
        "duration": "3:20",
        "trending_rank": 1,
        "spotify_url": "https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b"
      }
    }
  }
  ```

---

### Task 4: stdio Transport vs. HTTP Transport
- **Goal**: Compare `stdio` and `HTTP` transports in MCP and update the client to communicate over `stdio` pipes.
- **Documentation**: See [`task4_transport_comparison.md`](file:///d:/tops%20data/Agentic%20AI/Assignment/Session%2014/task4_transport_comparison.md).
- **Client Execution**:
  The client automatically launches the server as a child process, pipes the JSON-RPC payload through `stdin`, and reads the response through `stdout`.
- **To Run**:
  ```bash
  python task4_stdio_client.py
  ```
- **Key Takeaway**:
  - `stdio`: Zero latency, no open ports, ideal for local desktop AI (Claude Desktop, Cursor).
  - `HTTP`: Scalable, multi-tenant, ideal for remote cloud agents and microservices.

---

### Task 5: Custom MCP Prompt for 'get_movie_showtimes'
- **Goal**: Draft a custom BookMyShow-style MCP Prompt, document how to integrate it, and implement the server and test client.
- **Documentation**: See [`task5_movie_showtimes.md`](file:///d:/tops%20data/Agentic%20AI/Assignment/Session%2014/task5_movie_showtimes.md).
- **Features**:
  - Prompt: `get_movie_showtimes` (arguments: `movie_name`, `city`, `date`, `preferred_format`, `time_slot`).
  - Supports `prompts/list` and `prompts/get`.
  - Companion Tool: `fetch_movie_showtimes` querying live cinema showtimes (IMAX Laser, 4DX, seat categories, pricing in INR).
- **To Run**:
  ```bash
  # Terminal 1: Run Task 5 server
  python task5_movie_showtimes_server.py

  # Terminal 2: Run Task 5 test client
  python task5_test_prompt.py
  ```
