"""
============================================================
 GRAPH ALGORITHM — Minimum Spanning Tree
 Kruskal's Algorithm + Union-Find (DSU)
============================================================

 Problem Formulation:
   Platforms = Graph Nodes
   Edge weight = logistics cost between two platforms
   MST = minimum cost delivery network connecting all platforms

 Kruskal's Algorithm:
   1. Build all edges (P×(P-1)/2 edges for complete graph)
   2. Sort edges by weight ascending
   3. Add edge if it doesn't form a cycle (Union-Find check)
   4. Stop when MST has (P-1) edges

 Time Complexity:  O(E log E) = O(P² log P)
 Space Complexity: O(P + E)

 Union-Find with Path Compression + Union by Rank → O(α(n))
============================================================
"""


# ── Union-Find (Disjoint Set Union) ─────────────────────────────────

class UnionFind:
    """
    Union-Find with Path Compression + Union by Rank.
    Each operation is amortized O(α(n)) ≈ O(1).
    """
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank   = [0] * n
        self.components = n

    def find(self, x):
        """Find root with PATH COMPRESSION."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x, y):
        """
        Union by rank. Returns True if merged (no cycle),
        False if already in same set (cycle detected).
        """
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False   # same component → would form cycle!

        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx]  += 1

        self.components -= 1
        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)


# ── Platform graph ──────────────────────────────────────────────────

PLATFORM_META = {
    "amazon":   {"baseCost": 0,   "city": "Mumbai",    "deliveryDays": 2},
    "flipkart": {"baseCost": 0,   "city": "Bangalore", "deliveryDays": 3},
    "meesho":   {"baseCost": 49,  "city": "Gurugram",  "deliveryDays": 5},
    "snapdeal": {"baseCost": 99,  "city": "New Delhi", "deliveryDays": 4},
    "myntra":   {"baseCost": 0,   "city": "Bangalore", "deliveryDays": 3}
}


def _edge_weight(p1, p2):
    """Compute edge weight between two platforms."""
    m1 = PLATFORM_META.get(p1, {})
    m2 = PLATFORM_META.get(p2, {})
    day_gap  = abs(m1.get("deliveryDays", 3) - m2.get("deliveryDays", 3))
    cost_diff = abs(m1.get("baseCost", 0)   - m2.get("baseCost", 0))
    return day_gap * 15 + cost_diff + 40  # 40 = base transition cost


def kruskal_mst(platforms):
    """
    Kruskal's Minimum Spanning Tree Algorithm.

    Args:
        platforms: list of platform names

    Returns:
        dict with MST edges, total weight, steps
    """
    n = len(platforms)
    idx = {p: i for i, p in enumerate(platforms)}

    # Step 1: Build all edges O(P²)
    all_edges = []
    for i in range(n):
        for j in range(i + 1, n):
            w = _edge_weight(platforms[i], platforms[j])
            all_edges.append({
                "u": i, "v": j,
                "u_name": platforms[i],
                "v_name": platforms[j],
                "weight": w
            })

    # Step 2: Sort edges by weight O(E log E)
    sorted_edges = sorted(all_edges, key=lambda e: e["weight"])

    # Step 3: Kruskal's with Union-Find
    uf        = UnionFind(n)
    mst_edges = []
    rejected  = []
    total_wt  = 0
    steps     = []

    for edge in sorted_edges:
        if uf.union(edge["u"], edge["v"]):
            mst_edges.append(edge)
            total_wt += edge["weight"]
            steps.append({
                "action":      "ACCEPTED",
                "edge":        f"{edge['u_name']} — {edge['v_name']}",
                "weight":      edge["weight"],
                "reason":      "No cycle formed — MST edge added",
                "mst_count":   len(mst_edges)
            })
            if len(mst_edges) == n - 1:
                break
        else:
            rejected.append(edge)
            steps.append({
                "action":      "REJECTED",
                "edge":        f"{edge['u_name']} — {edge['v_name']}",
                "weight":      edge["weight"],
                "reason":      "Cycle detected — Union-Find roots match",
                "mst_count":   len(mst_edges)
            })

    # Adjacency list
    adj = {p: [] for p in platforms}
    for e in mst_edges:
        adj[e["u_name"]].append({"to": e["v_name"], "weight": e["weight"]})
        adj[e["v_name"]].append({"to": e["u_name"], "weight": e["weight"]})

    e_total = len(all_edges)
    import math
    ops = round(e_total * math.log2(e_total)) if e_total > 1 else 1

    return {
        "algorithm":      "Kruskal's MST with Union-Find (Path Compression + Union by Rank)",
        "complexity":     f"O(E log E) = O({e_total} × log {e_total}) ≈ O({ops} operations)",
        "platforms":      platforms,
        "total_edges":    e_total,
        "mst_edges":      mst_edges,
        "rejected_edges": rejected,
        "total_weight":   total_wt,
        "adjacency_list": adj,
        "steps":          steps,
        "interpretation": f"MST connects all {n} platforms with minimum logistics cost of {total_wt} units"
    }
