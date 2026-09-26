# Session 14 – Task 5: Custom MCP Prompt for 'get_movie_showtimes' (BookMyShow-Style)

## 1. Overview of Prompts in MCP

In the **Model Context Protocol (MCP)** specification:
- **Tools** are callable routines executed by the LLM agent to fetch live data or perform side effects.
- **Prompts** are structured, parameterised templates published by an MCP server to guide the user and the LLM through specific workflows. They can be surfaced to users as slash commands (e.g. `/get_movie_showtimes`) or selected programmatically by an AI agent.

When a client queries the MCP server:
1. `prompts/list`: Returns metadata and input argument specifications for all registered prompts.
2. `prompts/get`: Accepts argument values from the client and returns a sequence of context-rich `PromptMessage` objects (with role `user` or `assistant`) designed to guide the LLM.

---

## 2. Drafted Custom MCP Prompt Specification

### Prompt Metadata
- **Name**: `get_movie_showtimes`
- **Description**: *"BookMyShow-style cinema assistant prompt to query live movie showtimes, cinema halls, audio/visual formats (IMAX, 4DX, 2D), seat categories, and ticket pricing."*

### Argument Schema
| Argument Name | Type | Required | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `movie_name` | `string` | **Yes** | Title of the movie to query | `"Dune: Part Two"` |
| `city` | `string` | **Yes** | City or metropolitan region | `"Mumbai"` |
| `date` | `string` | No (default: `"today"`) | Target show date | `"today"`, `"tomorrow"`, `"2026-10-02"` |
| `preferred_format` | `string` | No (default: `"Any"`) | Cinema format | `"IMAX 2D"`, `"4DX"`, `"3D"`, `"2D"` |
| `time_slot` | `string` | No (default: `"Any"`) | Preferred time window | `"Morning"`, `"Afternoon"`, `"Evening"`, `"Night"` |

---

## 3. The Prompt Template & Content

When `prompts/get` is called with arguments `{"movie_name": "Dune: Part Two", "city": "Mumbai", "date": "today", "preferred_format": "IMAX 2D", "time_slot": "Evening"}`, the server returns the following structured `user` message:

```markdown
You are a BookMyShow Cinema Concierge Assistant.

### USER QUERY CONTEXT:
- Movie Title:        {movie_name}
- Target City:        {city}
- Booking Date:       {date}
- Preferred Format:   {preferred_format}
- Preferred Slot:     {time_slot}

### YOUR OBJECTIVE:
Assist the user in discovering, comparing, and selecting movie tickets for '{movie_name}' in {city}.

### INSTRUCTIONS FOR ASSISTANT:
1. QUERY LIVE SHOWTIMES:
   Use the MCP tool 'fetch_movie_showtimes' with the provided parameters (movie_name='{movie_name}', city='{city}', date='{date}', format='{preferred_format}').

2. PRESENT SHOWTIMES ELEGANTLY:
   Group results by Cinema Hall (e.g., PVR ICON Phoenix Palladium, INOX Megaplex, Cinepolis).
   For each cinema, display:
   - Available show timings (e.g., 04:30 PM, 07:15 PM, 10:30 PM).
   - Screen format (e.g., IMAX Laser 2D, Atmos 7.1).
   - Seat categories & live pricing in INR (₹) (e.g., Recliner: ₹650 | Prime: ₹380 | Classic: ₹250).
   - Availability status (🟢 Available, 🟡 Filling Fast, 🔴 Almost Full).

3. USER RECOMMENDATION:
   If '{preferred_format}' or '{time_slot}' matches specific shows, highlight them first with a ⭐ 'Best Match' badge.

4. CALL TO ACTION:
   Ask the user how many tickets they would like to book and which showtime/cinema they prefer to proceed to seat selection.
```

---

## 4. How to Integrate this Prompt into an MCP Server

There are two primary ways to integrate custom prompts into an MCP server using Python:

### Approach A: Using the High-Level `FastMCP` API (Official Python SDK)

```python
from mcp.server.fastmcp import FastMCP
from mcp.types import PromptMessage, TextContent

mcp = FastMCP("BookMyShow-MCP-Server")

@mcp.prompt("get_movie_showtimes")
def get_movie_showtimes(
    movie_name: str,
    city: str,
    date: str = "today",
    preferred_format: str = "Any",
    time_slot: str = "Any"
) -> list[PromptMessage]:
    """BookMyShow movie showtime assistant prompt."""
    prompt_text = f"""
You are a BookMyShow Cinema Concierge Assistant.
Help the user find showtimes for '{movie_name}' in {city} for {date}.
Preferred Format: {preferred_format} | Time Slot: {time_slot}.

1. Call the 'fetch_movie_showtimes' tool.
2. Group showtimes by cinema hall.
3. Show seat categories (Classic, Prime, Recliner) with pricing in INR.
4. Highlight top matches for the user's preferred format and time.
"""
    return [
        PromptMessage(
            role="user",
            content=TextContent(type="text", text=prompt_text.strip())
        )
    ]
```

### Approach B: Using JSON-RPC Protocol Handlers (Wire Protocol)

When implementing or extending a standard JSON-RPC 2.0 MCP server:
1. **Handle `prompts/list`**:
   Return the metadata, description, and argument schema for `get_movie_showtimes`.
2. **Handle `prompts/get`**:
   Extract `name` and `arguments` from `params`, interpolate parameters into the structured prompt template, and return the `PromptMessage` array.
3. **Register Accompanying Tool (`fetch_movie_showtimes`)**:
   Provide the tool that the LLM agent can call when executing the prompt, closing the loop between prompt guidance and live execution.

---

## 5. End-to-End Client & Agent Workflow

```
+------------+               +------------------+               +------------------+
| User / LLM |               |    MCP Client    |               |    MCP Server    |
+------------+               +------------------+               +------------------+
      |                               |                                   |
      |-- 1. List Prompts ----------->|-- JSON-RPC 'prompts/list' ------->|
      |                               |<-- Returns available prompts -----|
      |                               |                                   |
      |-- 2. Select 'get_movie_showtimes'                                |
      |      with movie='Dune', city='Mumbai'                             |
      |                               |-- JSON-RPC 'prompts/get' -------->|
      |                               |<-- Returns PromptMessages --------|
      |                               |                                   |
      |<-- 3. Prompt injected into LLM Context                            |
      |                                                                   |
      |-- 4. LLM calls 'fetch_movie_showtimes' tool --------------------->|
      |<-- 5. Server returns cinema showtimes & seat pricing -------------|
      |                                                                   |
      |-- 6. LLM presents formatted BookMyShow schedule to user ----------|
```
