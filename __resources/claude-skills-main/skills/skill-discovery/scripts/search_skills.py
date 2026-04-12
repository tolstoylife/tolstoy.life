#!/usr/bin/env python3
"""
Search claude-plugins.dev/skills API
Provides deterministic skill discovery via web search
"""
import sys
import urllib.request
import urllib.parse
import json
from typing import List, Dict, Optional


def search_skills(query: str, sort: str = "relevance", limit: int = 10) -> List[Dict]:
    """
    Search for skills on claude-plugins.dev

    Args:
        query: Search query string
        sort: Sort order ('relevance', 'downloads', 'stars')
        limit: Maximum number of results to return

    Returns:
        List of skill dictionaries with keys: name, identifier, description, downloads, author
    """
    # Construct search URL
    base_url = "https://claude-plugins.dev/skills"
    params = {}
    if query:
        params['q'] = query
    if sort and sort != "relevance":
        params['sort'] = sort

    url = base_url
    if params:
        url = f"{base_url}?{urllib.parse.urlencode(params)}"

    try:
        # Make HTTP request
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'skill-discovery/1.0'}
        )

        with urllib.request.urlopen(req, timeout=5) as response:
            # For now, return URL since actual parsing would require HTML scraping
            # In practice, this would parse the HTML response
            return [{
                "search_url": url,
                "note": "Use WebFetch with this URL and prompt: 'Extract all skills with their names, identifiers (@owner/repo/name), descriptions, and download counts'"
            }]

    except urllib.error.URLError as e:
        print(f"Error fetching skills: {e}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return []


def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: search_skills.py <query> [--sort=downloads|stars|relevance] [--limit=N]")
        print("Example: search_skills.py 'testing debugging'")
        sys.exit(1)

    query = sys.argv[1]
    sort = "relevance"
    limit = 10

    # Parse additional arguments
    for arg in sys.argv[2:]:
        if arg.startswith("--sort="):
            sort = arg.split("=")[1]
        elif arg.startswith("--limit="):
            limit = int(arg.split("=")[1])

    results = search_skills(query, sort, limit)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
