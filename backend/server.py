"""
============================================================
 SMART SHOPPING CART OPTIMIZER — Python Backend Server
 Pure Python stdlib: http.server + json
 Serves frontend static files + REST API on port 5000
============================================================
"""

import sys
import os
import json
import re
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# ── Path setup ─────────────────────────────────────────────────────
BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")

sys.path.insert(0, BASE_DIR)

from data.products import PRODUCTS, PLATFORM_META
from algorithms.merge_sort import (
    merge_sort, best_price_key, platform_price_key,
    rating_key, review_count_key, relevance_key
)
from algorithms.greedy  import greedy_cheapest_platform, fractional_knapsack
from algorithms.tsp     import optimize_platform_order
from algorithms.mst     import kruskal_mst
from live_scraper import search_live_products

# In-memory session cache to bridge dynamic internet searches with cart logic
LIVE_CACHE = {p["id"]: p for p in PRODUCTS}
SCRAPE_CACHE = {}

def get_cached_or_scrape(q):
    if q in SCRAPE_CACHE:
        return SCRAPE_CACHE[q]
    res = search_live_products(q)
    if res:
        SCRAPE_CACHE[q] = res
    return res

# ── Cart Optimizer ─────────────────────────────────────────────────

def optimize_cart(cart_items, budget=None):
    """Run all DAA algorithms on cart items."""
    if not cart_items:
        return {"error": "Cart is empty"}

    import time
    start = time.time()

    # Step 1: Greedy platform selection
    greedy = greedy_cheapest_platform(cart_items)

    # Step 2: Group items by platform for TSP
    platform_assignments = {}
    for sel in greedy["selections"]:
        p = sel["platform"]
        platform_assignments.setdefault(p, [])
        platform_assignments[p].append(sel["product_id"])

    # Step 3: TSP — optimal platform visit order
    tsp = optimize_platform_order(platform_assignments, PLATFORM_META)

    # Step 4: MST — delivery network
    active = [p for p, ids in platform_assignments.items() if ids]
    mst    = kruskal_mst(active) if active else {"mst_edges": [], "steps": [], "total_weight": 0}

    # Step 5: Fractional knapsack (if budget given)
    knapsack = None
    if budget and budget > 0:
        knapsack = fractional_knapsack(cart_items, budget)

    # Step 6: Sort with Merge Sort
    sorted_result = merge_sort(cart_items, best_price_key)

    # Step 7: Costs comparison
    naive_cost = 0
    for item in cart_items:
        ap = item["platforms"].get("amazon", {})
        if ap.get("available"):
            naive_cost += ap["price"] + ap["deliveryCost"]
        else:
            prices = [p["price"] + p["deliveryCost"] for p in item["platforms"].values() if p.get("available")]
            naive_cost += min(prices) if prices else 0

    optimized_cost = greedy["total_cost"]
    savings        = naive_cost - optimized_cost
    savings_pct    = round((savings / naive_cost * 100), 1) if naive_cost else 0
    exec_ms        = round((time.time() - start) * 1000)

    return {
        "success": True,
        "summary": {
            "item_count":      len(cart_items),
            "naive_cost":      naive_cost,
            "optimized_cost":  optimized_cost,
            "total_savings":   savings,
            "savings_percent": savings_pct,
            "platforms_used":  active,
            "execution_ms":    exec_ms
        },
        "algorithms": {
            "step1_greedy":  greedy,
            "step2_tsp":     tsp,
            "step3_mst":     mst,
            "step4_knapsack": knapsack,
            "step5_sort": {
                "algorithm":         "Merge Sort (Divide & Conquer)",
                "complexity":        "O(n log n)",
                "total_comparisons": sorted_result["total_comparisons"],
                "sorted": [
                    {
                        "id":   p["id"],
                        "name": p["name"],
                        "best_price": min(
                            (pl["price"] + pl["deliveryCost"])
                            for pl in p["platforms"].values() if pl.get("available")
                        )
                    }
                    for p in sorted_result["sorted"]
                ],
                "steps": sorted_result["steps"]
            }
        },
        "platform_assignments": platform_assignments,
        "recommended_order": tsp.get("optimal_order", active),
        "complexity_analysis": {
            "mergeSort":         "O(n log n) — Divide & Conquer",
            "greedySelection":   "O(n × P) where P=5 platforms",
            "fractionalKnapsack":"O(n log n) — Greedy with sorting",
            "tspHeldKarp":       "O(2^P × P²) — Bitmask DP",
            "kruskalMST":        "O(E log E) with Union-Find",
            "overall":           "O(2^P × P²) — TSP dominates for small P"
        }
    }


# ── HTTP Handler ────────────────────────────────────────────────────

class SSCOHandler(SimpleHTTPRequestHandler):
    """Custom handler: serves static files + handles /api/* routes."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=FRONTEND_DIR, **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    # ── Static files ──────────────────────────────────────────────
    def _set_cors(self):
        self.send_header("Access-Control-Allow-Origin",  "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors()
        self.end_headers()

    # ── JSON response helper ────────────────────────────────────
    def _json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type",   "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._set_cors()
        self.end_headers()
        self.wfile.write(body)

    # ── Read POST body ──────────────────────────────────────────
    def _read_json_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length:
            raw = self.rfile.read(length)
            return json.loads(raw.decode("utf-8"))
        return {}

    # ── Route: GET /api/products ────────────────────────────────
    def _api_get_products(self, query):
        sort_by  = query.get("sort", ["relevance"])[0]
        platform = query.get("platform", ["amazon"])[0]
        search   = query.get("search",   [""])[0].lower()
        category = query.get("category", [""])[0].lower()

        q = search if search else (category if category else "laptop")
        products = get_cached_or_scrape(q)
        
        if not products:
            products = list(PRODUCTS)
            if search:
                filtered = [
                    p for p in products
                    if search in p["name"].lower()
                    or search in p["category"].lower()
                ]
                products = filtered if filtered else list(PRODUCTS)[:8]
            if category:
                products = [p for p in products if p["category"].lower() == category]

        # Add to session cache so /optimize can find it later
        for p in products:
            LIVE_CACHE[p["id"]] = p

        # Merge Sort with chosen comparator
        key_map = {
            "price_asc":  (platform_price_key(platform), False),
            "price_desc": (platform_price_key(platform), True),
            "rating":     (rating_key,       False),
            "reviews":    (review_count_key, False),
            "best_price": (best_price_key,   False),
            "relevance":  (relevance_key,    False),
        }
        key_fn, reverse = key_map.get(sort_by, (relevance_key, False))
        result = merge_sort(products, key_fn, reverse)

        self._json({
            "success": True,
            "count":   len(result["sorted"]),
            "sorted_by": sort_by,
            "algorithm": {
                "name":              "Merge Sort",
                "type":              "Divide and Conquer",
                "complexity":        "O(n log n)",
                "total_comparisons": result["total_comparisons"],
                "steps":             result["steps"][:5]
            },
            "products": result["sorted"]
        })

    # ── Route: GET /api/products/<id> ───────────────────────────
    def _api_get_product(self, pid):
        product = LIVE_CACHE.get(int(pid))
        if not product:
            self._json({"error": "Product not found"}, 404)
        else:
            self._json({"success": True, "product": product})

    # ── Route: GET /api/categories ──────────────────────────────
    def _api_get_categories(self):
        cats = sorted(set(p["category"] for p in PRODUCTS))
        self._json({"success": True, "categories": cats})

    # ── Route: GET /api/optimize/mst ────────────────────────────
    def _api_get_mst(self):
        result = kruskal_mst(list(PLATFORM_META.keys()))
        self._json(result)

    # ── Route: GET /api/algorithms ──────────────────────────────
    def _api_get_algorithms(self):
        self._json({
            "algorithms": [
                {
                    "name": "Merge Sort",
                    "type": "Divide and Conquer",
                    "use":  "Sorting products by price, rating, relevance",
                    "time": "O(n log n)", "space": "O(n)"
                },
                {
                    "name": "Greedy Platform Selection",
                    "type": "Greedy",
                    "use":  "Selecting cheapest platform per cart item",
                    "time": "O(n × P) where P=5", "space": "O(n)"
                },
                {
                    "name": "Fractional Knapsack",
                    "type": "Greedy",
                    "use":  "Budget-constrained product selection",
                    "time": "O(n log n)", "space": "O(n)"
                },
                {
                    "name": "Held-Karp TSP",
                    "type": "Dynamic Programming",
                    "use":  "Optimal platform visit ordering",
                    "time": "O(2^P × P²)", "space": "O(2^P × P)"
                },
                {
                    "name": "Kruskal's MST",
                    "type": "Graph Algorithm",
                    "use":  "Minimum cost delivery network",
                    "time": "O(E log E)", "space": "O(V + E)"
                }
            ]
        })

    # ── Route: GET /api/health ──────────────────────────────────
    def _api_health(self):
        self._json({
            "status":     "OK",
            "message":    "SSCO Python Backend running",
            "algorithms": ["Merge Sort", "Greedy", "Fractional Knapsack", "TSP", "Kruskal MST"]
        })

    # ── POST: /api/optimize ─────────────────────────────────────
    def _api_post_optimize(self):
        body          = self._read_json_body()
        cart_item_ids = body.get("cartItemIds", [])
        budget        = body.get("budget")

        cart_items = [LIVE_CACHE[int(i)] for i in cart_item_ids if int(i) in LIVE_CACHE]
        if not cart_items:
            self._json({"error": "No valid products in cart"}, 400)
            return

        result = optimize_cart(cart_items, int(budget) if budget else None)
        self._json(result)

    # ── POST: /api/optimize/greedy ──────────────────────────────
    def _api_post_greedy(self):
        body          = self._read_json_body()
        cart_item_ids = body.get("cartItemIds", [])
        cart_items    = [LIVE_CACHE[int(i)] for i in cart_item_ids if int(i) in LIVE_CACHE]
        self._json(greedy_cheapest_platform(cart_items))

    # ── POST: /api/optimize/knapsack ────────────────────────────
    def _api_post_knapsack(self):
        body   = self._read_json_body()
        budget = body.get("budget", 100000)
        self._json(fractional_knapsack(list(LIVE_CACHE.values()), int(budget)))

    # ── GET routing ─────────────────────────────────────────────
    def do_GET(self):
        parsed = urlparse(self.path)
        path   = parsed.path.rstrip("/")
        query  = parse_qs(parsed.query)

        # API routes
        if path == "/api/health":
            self._api_health(); return
        if path == "/api/algorithms":
            self._api_get_algorithms(); return
        if path == "/api/products":
            self._api_get_products(query); return
        if path == "/api/categories":
            self._api_get_categories(); return
        if path == "/api/optimize/mst":
            self._api_get_mst(); return

        m = re.match(r"^/api/products/(\d+)$", path)
        if m:
            self._api_get_product(m.group(1)); return

        # For clean URLs like /products, /cart → serve .html
        clean_routes = {
            "":           "/index.html",
            "/products":  "/products.html",
            "/cart":      "/cart.html",
            "/compare":   "/compare.html",
            "/algorithms":"/algorithms.html"
        }
        if path in clean_routes:
            self.path = clean_routes[path]
            super().do_GET()
            return

        # Fallback: serve static file
        super().do_GET()

    # ── POST routing ────────────────────────────────────────────
    def do_POST(self):
        parsed = urlparse(self.path)
        path   = parsed.path.rstrip("/")

        if path == "/api/optimize":
            self._api_post_optimize()
        elif path == "/api/optimize/greedy":
            self._api_post_greedy()
        elif path == "/api/optimize/knapsack":
            self._api_post_knapsack()
        else:
            self._json({"error": "Not found"}, 404)

    # ── Quiet logs ──────────────────────────────────────────────
    def log_message(self, fmt, *args):
        # Color output
        method = args[0] if args else ""
        code   = args[1] if len(args) > 1 else ""
        status = str(code)
        color  = "\033[32m" if status.startswith("2") else "\033[33m" if status.startswith("3") else "\033[31m"
        reset  = "\033[0m"
        print(f"  {color}{method}{reset} [{code}]  {self.path[:60]}")


# ── Main ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    PORT   = int(os.environ.get("PORT", 5000))
    server = ThreadingHTTPServer(("0.0.0.0", PORT), SSCOHandler)

    print("\n" + "="*56)
    print("  🛒  SMART SHOPPING CART OPTIMIZER — Python Server")
    print(f"  🚀  Running at: http://0.0.0.0:{PORT}")
    print("  📊  DAA: MergeSort | Greedy | Knapsack | TSP | MST")
    print("="*56 + "\n")


    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n  ⏹  Server stopped.\n")
        server.shutdown()
