# Smart Shopping Cart Optimizer (SSCO)

DAA project that compares shopping products and demonstrates algorithmic cart optimization with a Python backend and vanilla HTML/CSS/JavaScript frontend.

## Features

- Product browsing, filtering, cart, and comparison pages.
- Merge Sort for product ordering.
- Greedy cheapest-platform cart optimization.
- Fractional Knapsack for budget-based selection.
- Held-Karp TSP for platform order demonstration.
- Kruskal MST for delivery/logistics network demonstration.
- Playwright-based live product discovery with sample-data fallback.

## Run Locally

```powershell
pip install -r requirements.txt
playwright install chromium
python backend/server.py
```

Then open `http://localhost:5000`.

## Layout

```text
backend/   Python server, scraper, data, and algorithms
frontend/  Static HTML, CSS, and JavaScript
```

## Notes

- The backend writes `backend/search_cache.json` at runtime and it is ignored by Git.
- Generated Python bytecode files are ignored by Git.
