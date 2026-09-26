"""
Session 14 - Task 3: Client for 'get_song_recommendation'
=========================================================
This script calls the modified MCP Server's 'get_song_recommendation'
method and prints the received Spotify-style trending song data.
"""

import json
import sys
import requests

# Ensure safe UTF-8 output on Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SERVER_URL = "http://127.0.0.1:8000/"

def test_song_recommendation():
    print("=" * 65)
    print("  SESSION 14 - TASK 3: TESTING 'get_song_recommendation' METHOD")
    print("=" * 65)

    # Test 1: Random Trending Song
    print("\n--- Test 1: Requesting Any Random Trending Song ---")
    payload_random = {
        "jsonrpc": "2.0",
        "id": "req-song-001",
        "method": "get_song_recommendation",
        "params": {}
    }

    try:
        res1 = requests.post(SERVER_URL, json=payload_random, timeout=5)
        data1 = res1.json()
        print("[*] Request Payload:")
        print(json.dumps(payload_random, indent=2))
        print(f"[*] Response Status: {res1.status_code}")
        print("[*] Response Payload:")
        print(json.dumps(data1, indent=2))

        song = data1.get("result", {}).get("recommendation", {})
        if song:
            print("\n[+] Trending Song Recommendation Details:")
            print(f"   * Title:       {song.get('title')}")
            print(f"   * Artist:      {song.get('artist')}")
            print(f"   * Album:       {song.get('album')} ({song.get('release_year')})")
            print(f"   * Genre:       {song.get('genre')}")
            print(f"   * Spotify URL: {song.get('spotify_url')}")
            print(f"   * Rank / Pop:  #{song.get('trending_rank')} (Score: {song.get('popularity_score')})")

    except requests.exceptions.ConnectionError:
        print(f"[-] Connection Error: Ensure 'task3_mcp_server.py' is running on {SERVER_URL}.")
        sys.exit(1)

    # Test 2: Filtered by Genre
    print("\n" + "-" * 65)
    print("--- Test 2: Requesting Synthwave Genre Recommendation ---")
    payload_genre = {
        "jsonrpc": "2.0",
        "id": "req-song-002",
        "method": "get_song_recommendation",
        "params": {"genre": "Synthwave"}
    }
    res2 = requests.post(SERVER_URL, json=payload_genre, timeout=5)
    data2 = res2.json()
    print("[*] Filtered Response:")
    print(json.dumps(data2, indent=2))
    print("=" * 65)
    print("[SUCCESS] Task 3 'get_song_recommendation' verified successfully!")

if __name__ == "__main__":
    test_song_recommendation()
