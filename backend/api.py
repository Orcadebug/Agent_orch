import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any

app = FastAPI(title="Visual PR Activity Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from github_ingestor import ingest_prs

import time
import re

# Simple in-memory cache
# Format: { "repo_name": { "timestamp": float, "data": dict } }
cache: Dict[str, Dict[str, Any]] = {}
CACHE_TTL = 3600  # 1 hour in seconds

def clean_repo_input(raw_input: str) -> str:
    if not raw_input:
        return ""
    
    raw_input = raw_input.strip()
    
    # Try to extract from a github URL
    # Matches http://github.com/owner/repo or https://www.github.com/owner/repo
    pattern = r"(?:https?:\/\/)?(?:www\.)?github\.com\/([^\/]+\/[^\/]+?)(?:\.git|\/|$|\?)"
    match = re.search(pattern, raw_input, re.IGNORECASE)
    
    if match:
        repo = match.group(1)
        # remove trailing .git just in case the regex caught it
        if repo.endswith('.git'):
            repo = repo[:-4]
        return repo
    
    return raw_input


@app.get("/api/graph")
def get_graph(repo: str = "vitali87/code-graph-rag") -> Dict[str, Any]:
    # Clean the input in case a raw URL was passed directly to the API
    repo = clean_repo_input(repo)
    
    current_time = time.time()
    
    # Check cache first
    if repo in cache:
        cached_entry = cache[repo]
        if current_time - cached_entry["timestamp"] < CACHE_TTL:
            print(f"Returning cached data for {repo}")
            return cached_entry["data"]

    try:
        # Fetch directly from github using the ingestor
        data = ingest_prs(repo)
        
        # Save to cache if we got real data
        if data and len(data.get("nodes", [])) > 0:
            cache[repo] = {
                "timestamp": current_time,
                "data": data
            }
            
        return data
    except Exception as e:
        print(f"Error fetching repo {repo}: {e}")
        return {"nodes": [], "edges": []}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
