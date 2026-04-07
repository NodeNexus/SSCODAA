"""
============================================================
 GREEDY ALGORITHMS
 1) Cheapest-Platform Greedy  —  O(n × P)
 2) Fractional Knapsack       —  O(n log n)
============================================================

 Greedy Strategy: At each step, make the locally optimal
 choice hoping it leads to globally optimal solution.

 Fractional Knapsack IS greedy-solvable (items divisible).
============================================================
"""
import math


PLATFORMS = ["amazon", "flipkart", "meesho", "snapdeal", "myntra"]


def greedy_cheapest_platform(cart_items):
    """
    GREEDY: Select cheapest available platform per cart item.

    Algorithm:
      For each product, scan all platforms → pick min(price + deliveryCost)
      This is the GREEDY CHOICE: locally optimal = globally optimal
      for independent products (no shared platform constraints).

    Time Complexity: O(n × P) where n = items, P = platforms (5)
    Space Complexity: O(n)
    """
    steps = []
    total_greedy = 0
    total_naive  = 0   # baseline = Amazon

    selections = []

    for idx, product in enumerate(cart_items):
        best_platform = None
        best_cost     = float("inf")
        platform_costs = {}

        # Naive cost = Amazon price
        amazon_p = product["platforms"].get("amazon", {})
        naive_cost = (
            amazon_p["price"] + amazon_p["deliveryCost"]
            if amazon_p.get("available") else float("inf")
        )

        # Greedy scan
        for platform in PLATFORMS:
            p = product["platforms"].get(platform, {})
            if p.get("available"):
                eff = p["price"] + p["deliveryCost"]
                platform_costs[platform] = eff
                if eff < best_cost:
                    best_cost     = eff
                    best_platform = platform

        if best_platform is None:
            continue

        total_greedy += best_cost
        total_naive  += best_cost if naive_cost == float("inf") else naive_cost

        steps.append({
            "step":          idx + 1,
            "product":       product["name"],
            "platform_costs": platform_costs,
            "greedy_choice": best_platform,
            "greedy_cost":   best_cost,
            "naive_cost":    None if naive_cost == float("inf") else naive_cost,
            "saving":        0 if naive_cost == float("inf") else max(0, naive_cost - best_cost)
        })

        selections.append({
            "product":      product["name"],
            "product_id":   product["id"],
            "platform":     best_platform,
            "price":        product["platforms"][best_platform]["price"],
            "delivery_cost":product["platforms"][best_platform]["deliveryCost"],
            "effective_cost": best_cost
        })

    return {
        "algorithm":   "Greedy — Cheapest Platform",
        "complexity":  "O(n × P) where P = 5 platforms",
        "selections":  selections,
        "total_cost":  total_greedy,
        "naive_cost":  total_naive,
        "savings":     total_naive - total_greedy,
        "steps":       steps
    }


def fractional_knapsack(products, budget):
    """
    FRACTIONAL KNAPSACK — Greedy by value/weight ratio.

    Problem: Given a BUDGET, maximize VALUE (rating × log(reviews))
             while staying within budget. Items CAN be fractional.

    Algorithm:
      1. Compute ratio = value / price for each item
      2. Sort by ratio descending  ← GREEDY CHOICE
      3. Take as much of each item as budget allows

    Time Complexity: O(n log n) — sorting dominates
    Space Complexity: O(n)

    Greedy WORKS here because fractional items preserve
    the optimal substructure property.
    """
    if not budget or budget <= 0:
        return {"error": "Invalid budget"}

    # Step 1: Compute value and ratio
    items = []
    for p in products:
        prices = [
            pl["price"] + pl["deliveryCost"]
            for pl in p["platforms"].values()
            if pl.get("available")
        ]
        if not prices:
            continue

        price = min(prices)
        value = p["rating"] * math.log10(p["reviewCount"] + 1) * 1000
        ratio = value / price if price else 0

        items.append({
            "id":    p["id"],
            "name":  p["name"],
            "price": price,
            "value": round(value),
            "ratio": round(ratio, 6),
            "fraction": 0
        })

    # Step 2: Sort by ratio descending (GREEDY CHOICE)
    # Using Python's built-in here just for knapsack ordering;
    # Merge Sort is used for product display sorting.
    items.sort(key=lambda x: -x["ratio"])

    # Step 3: Greedy selection
    remaining = budget
    total_value = 0
    selected = []
    steps = []

    for item in items:
        if remaining <= 0:
            break

        if item["price"] <= remaining:
            item["fraction"] = 1.0
            remaining        -= item["price"]
            total_value      += item["value"]
            action = "Full (1.0)"
        else:
            fraction          = remaining / item["price"]
            item["fraction"]  = round(fraction, 4)
            total_value       += item["value"] * fraction
            action            = f"Fraction ({fraction:.4f})"
            remaining         = 0

        steps.append({
            "item":        item["name"],
            "ratio":       item["ratio"],
            "taken":       action,
            "cost":        item["price"] if item["fraction"] == 1.0 else budget - remaining,
            "value":       round(item["value"] * item["fraction"]),
            "budget_left": remaining
        })
        selected.append(dict(item))

    return {
        "algorithm":      "Fractional Knapsack (Greedy)",
        "complexity":     "O(n log n)",
        "budget":         budget,
        "total_value":    round(total_value),
        "amount_spent":   budget - remaining,
        "budget_remaining": remaining,
        "selected":       selected,
        "steps":          steps
    }
