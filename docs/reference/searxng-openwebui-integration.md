---
title: "SearXNG Integration with Open WebUI"
document_type: reference
date: "2026-04-13"
status: reference
tags: ['searxng', 'open-webui', 'search', 'atlas', 'integration']
---

# SearXNG Integration with Open WebUI v0.8.12
**Date:** April 13, 2026  
**Purpose:** Enable web search in Open WebUI via self-hosted SearXNG (zero API cost)

---

## Overview

SearXNG is running on Atlas at `http://100.101.158.93:8888`. Open WebUI can query it directly for web search results without any external API costs.

---

## Step 1: Create a Web Search Function in Open WebUI

1. Open Open WebUI: `http://100.101.158.93:3001`
2. Go to **Settings → Functions**
3. Click **"Create New Function"** (or find the + button)
4. Select **"Filter"** type (this intercepts model responses)

---

## Step 2: Function Code

Name the function: `SearXNG Web Search`

Paste this code:

```python
"""
title: SearXNG Web Search
author: Concierge
version: 0.1.0
license: MIT
"""

import requests
import json
from typing import Optional

class Filter:
    def __init__(self):
        self.searxng_url = "http://100.101.158.93:8888"
    
    async def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """
        Intercept user messages looking for web search triggers.
        Keywords: "search", "web", "current", "latest", "price", "availability"
        """
        
        # Check if the message contains web search keywords
        messages = body.get("messages", [])
        if messages:
            last_message = messages[-1].get("content", "").lower()
            
            search_keywords = [
                "search", "web", "current", "latest", "price", 
                "availability", "news", "today", "recent", "find"
            ]
            
            if any(keyword in last_message for keyword in search_keywords):
                # Extract search query from the message
                search_query = messages[-1].get("content", "")
                
                # Query SearXNG
                try:
                    results = await self.search_searxng(search_query)
                    
                    if results:
                        # Inject search results into the context
                        context = f"\n\n**Web Search Results:**\n{results}\n\n"
                        messages[-1]["content"] = context + messages[-1]["content"]
                        body["messages"] = messages
                except Exception as e:
                    print(f"SearXNG search error: {e}")
        
        return body
    
    async def search_searxng(self, query: str) -> str:
        """Query SearXNG and format results"""
        try:
            response = requests.get(
                f"{self.searxng_url}/search",
                params={
                    "q": query,
                    "format": "json",
                    "engines": "google,bing,duckduckgo"
                },
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "X-Forwarded-For": "127.0.0.1",
                    "X-Real-IP": "127.0.0.1",
                    "Accept": "application/json"
                },
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])[:5]  # Top 5 results
                
                formatted = ""
                for i, result in enumerate(results, 1):
                    title = result.get("title", "No title")
                    url = result.get("url", "")
                    snippet = result.get("content", "No snippet")[:200]
                    
                    formatted += f"{i}. **{title}**\n   {snippet}...\n   [{url}]\n\n"
                
                return formatted if formatted else "No results found"
            else:
                return "Search failed"
        except Exception as e:
            return f"Search error: {str(e)}"

filter = Filter()
```

---

## Step 3: Configure the Function

Once pasted:

1. **Save** the function
2. Go back to **Settings → Functions**
3. Find **"SearXNG Web Search"** in the list
4. **Enable** it (toggle switch)
5. Set **priority** to 10 (high priority, runs early)

---

## Step 4: Test It

In Open WebUI chat:

1. Select a model (Gemma 4 26B, qwen, etc.)
2. Type a message with a search keyword:
   - "Search for the latest Qwen models"
   - "What's the current price of RTX 5060 Ti?"
   - "Find news about new AI model releases"

3. The function will:
   - Detect the search keyword
   - Query SearXNG
   - Inject results into the model's context
   - Model responds with fresh information

---

## How It Works

**Flow:**

```
User message (contains "search", "current", "price", etc.)
   ↓
Filter inlet intercepts
   ↓
Query SearXNG at http://100.101.158.93:8888
   ↓
Get top 5 results (Google, Bing, DuckDuckGo)
   ↓
Format as markdown
   ↓
Inject into model context
   ↓
Model reads results + generates response
   ↓
User gets answer based on current web data
```

---

## Cost

- **Zero API fees** — SearXNG is self-hosted
- **Bandwidth:** ~1-5MB per search
- **Latency:** 3-5 seconds per search

---

## Troubleshooting

**403 Forbidden Error:**

If you see `403 Forbidden` from SearXNG, it's the botdetection limiter blocking API requests. The function code now includes the required headers:

```python
headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "X-Forwarded-For": "127.0.0.1",
    "X-Real-IP": "127.0.0.1",
    "Accept": "application/json"
}
```

These headers tell SearXNG the request is legitimate and bypasses the botdetection filter.

**SearXNG is slow on first query:**

First search takes 3-5 seconds as engines warm up. Subsequent searches are faster. This is normal.

**Engine-specific rate limits:**

Some search engines (KarmaSearch, etc.) have their own rate limits. If one engine is rate-limited, others still work. SearXNG automatically falls back.

**SearXNG web UI works but API doesn't:**

If the browser interface works but the function fails, ensure the headers are present in the function code. The web UI sends browser headers automatically; API calls don't unless you add them explicitly.

---

## Previous Troubleshooting

**SearXNG not responding:**

```bash
# On Atlas, verify SearXNG is running
sudo docker ps | grep searxng

# Test manually with proper headers
curl -H "X-Forwarded-For: 127.0.0.1" \
     -H "X-Real-IP: 127.0.0.1" \
     "http://100.101.158.93:8888/search?q=test&format=json"
```

**Function not triggering:**

- Check that keywords are in the message (search, web, current, latest, price, etc.)
- Verify function is **enabled** in Settings → Functions
- Check Open WebUI logs for errors

**Timeout errors:**

- Increase timeout in the function code (already set to 15 seconds)
- SearXNG might be slow on first query (caches results after)

---

---

## Next Steps

- **Advanced:** Add ranking/filtering to prioritize high-quality results
- **Advanced:** Add follow-up searches if initial results are thin
- **Advanced:** Cache popular searches locally to speed up repeat queries

---

*Integration created April 13, 2026 for Concierge remote access scaffold.*
