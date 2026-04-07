"""
============================================================
 DYNAMIC PROGRAMMING — Traveling Salesman Problem (TSP)
 Held-Karp Algorithm (Exact DP with Bitmask)
============================================================

 Problem Formulation for Shopping:
   Platforms = "cities" to visit (order from)
   Edge weight = delivery day diff × 10 + base switching cost
   TSP finds the optimal ORDER to purchase from platforms to
   minimize total logistics / delivery overhead.

 State:
   dp[mask][i] = min cost to have visited platforms in
   'mask' bitmask, currently at platform i

 Recurrence:
   dp[mask][i] = min over all j NOT in mask:
                 dp[mask ^ (1<<i)][j] + cost[j][i]

 Time Complexity:  O(2^n × n²)
 Space Complexity: O(2^n × n)

 For n = 5 platforms: 2^5 × 25 = 800 states — very fast!
============================================================
"""


def build_cost_matrix(platform_names, platform_data):
    """
    Build cost matrix between platforms.
    cost[i][j] = penalty for ordering from platform i then j.
    """
    n = len(platform_names)
    cost = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i == j:
                cost[i][j] = 0
                continue
            pi = platform_data.get(platform_names[i], {})
            pj = platform_data.get(platform_names[j], {})
            day_gap = abs(pi.get("deliveryDays", 3) - pj.get("deliveryDays", 3))
            cost[i][j] = day_gap * 10 + 50   # 50 = base platform switch cost
    return cost


def held_karp_tsp(platform_names, cost):
    """
    Held-Karp TSP using Bitmask Dynamic Programming.

    Args:
        platform_names: list of platform names
        cost: n×n cost matrix

    Returns:
        dict with optimal path, cost, and DP table sample
    """
    n = len(platform_names)

    if n == 0:
        return {"path": [], "path_names": [], "optimal_cost": 0, "dp_table_sample": []}
    if n == 1:
        return {"path": [0], "path_names": platform_names, "optimal_cost": 0, "dp_table_sample": []}

    INF       = float("inf")
    FULL_MASK = (1 << n) - 1

    # dp[mask][i] = min cost to visit platforms in mask, ending at i
    dp     = [[INF]  * n for _ in range(1 << n)]
    parent = [[-1]   * n for _ in range(1 << n)]

    # Base case: start at platform 0
    dp[1][0] = 0

    # Fill DP table
    for mask in range(1, 1 << n):
        for u in range(n):
            if not (mask & (1 << u)):
                continue
            if dp[mask][u] == INF:
                continue
            # Try extending to platform v
            for v in range(n):
                if mask & (1 << v):
                    continue  # already visited
                new_mask = mask | (1 << v)
                new_cost = dp[mask][u] + cost[u][v]
                if new_cost < dp[new_mask][v]:
                    dp[new_mask][v]     = new_cost
                    parent[new_mask][v] = u

    # Find best ending platform (no return to start for shopping)
    min_cost      = INF
    last_platform = -1
    for u in range(1, n):
        if dp[FULL_MASK][u] < min_cost:
            min_cost      = dp[FULL_MASK][u]
            last_platform = u

    # Reconstruct path via parent table
    path    = []
    mask    = FULL_MASK
    current = last_platform
    while current != -1:
        path.insert(0, current)
        prev    = parent[mask][current]
        mask    = mask ^ (1 << current)
        current = prev

    # Build DP table sample for visualization
    dp_sample = []
    for m in range(1, min(FULL_MASK + 1, 16)):
        for i in range(n):
            if dp[m][i] != INF:
                platforms_in_mask = [
                    platform_names[idx] for idx in range(n) if m & (1 << idx)
                ]
                dp_sample.append({
                    "mask":      bin(m)[2:].zfill(n),
                    "platforms": platforms_in_mask,
                    "end_at":    platform_names[i],
                    "cost":      dp[m][i]
                })

    return {
        "path":          path,
        "path_names":    [platform_names[i] for i in path],
        "optimal_cost":  0 if min_cost == INF else min_cost,
        "dp_table_sample": dp_sample[:10]
    }


def optimize_platform_order(platform_assignments, platform_meta):
    """
    Given a dict of {platform: [product_ids]}, run TSP to find
    the optimal ORDER to process platform orders.
    """
    active = [p for p, ids in platform_assignments.items() if ids]

    if not active:
        return {"error": "No active platforms"}

    if len(active) == 1:
        return {
            "algorithm":      "TSP — Held-Karp (Bitmask DP)",
            "complexity":     "O(2^n × n²)",
            "active_platforms": active,
            "optimal_order":  active,
            "optimal_cost":   0,
            "note":           "Only 1 platform — no ordering needed",
            "dp_table_sample": []
        }

    cost   = build_cost_matrix(active, platform_meta)
    result = held_karp_tsp(active, cost)

    n = len(active)
    ops = (2 ** n) * (n ** 2)

    return {
        "algorithm":       "TSP — Held-Karp (Bitmask DP)",
        "complexity":      f"O(2^{n} × {n}²) = O({ops} operations)",
        "active_platforms": active,
        "cost_matrix":     cost,
        "cost_matrix_labels": active,
        "optimal_order":   result["path_names"],
        "optimal_cost":    result["optimal_cost"],
        "dp_table_sample": result["dp_table_sample"],
        "interpretation":  f"Order platforms as: {' → '.join(result['path_names'])} for minimum transition overhead"
    }
