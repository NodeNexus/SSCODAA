"""
============================================================
 MERGE SORT — Divide and Conquer
============================================================
 Time Complexity:  O(n log n) — Best, Average, Worst
 Space Complexity: O(n)  — auxiliary array

 How it works:
  1. DIVIDE:   Split array into two halves → O(log n) levels
  2. CONQUER:  Recursively sort each half
  3. COMBINE:  Merge sorted halves via Two-Pointer technique

 Used for: Sorting products by price, rating, or relevance.
============================================================
"""
import math


def _merge(left, right, key_fn, reverse=False):
    """
    Merge two sorted lists.
    key_fn: function(item) -> comparable value
    Returns (merged_list, comparisons_count)
    """
    result = []
    i = j = 0
    comparisons = 0

    while i < len(left) and j < len(right):
        comparisons += 1
        lv = key_fn(left[i])
        rv = key_fn(right[j])
        if (lv <= rv) if not reverse else (lv >= rv):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Append remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    return result, comparisons


def merge_sort(arr, key_fn, reverse=False):
    """
    Manual Merge Sort — NO built-in sort() used.

    Args:
        arr: list of product dicts
        key_fn: function returning sortable value from item
        reverse: True for descending order

    Returns:
        dict with keys: sorted, total_comparisons, steps
    """
    total_comparisons = [0]
    steps = []

    def _sort(array, depth=0):
        if len(array) <= 1:
            return array

        mid = len(array) // 2
        left  = _sort(array[:mid],  depth + 1)
        right = _sort(array[mid:],  depth + 1)

        merged, comparisons = _merge(left, right, key_fn, reverse)
        total_comparisons[0] += comparisons

        # Record step for first 3 depth levels
        if depth <= 2:
            steps.append({
                "depth": depth,
                "left_size": len(left),
                "right_size": len(right),
                "merged_size": len(merged),
                "comparisons": comparisons,
                "sample": [item.get("name", str(item))[:20] for item in merged[:3]]
            })

        return merged

    sorted_arr = _sort(list(arr))
    return {
        "sorted": sorted_arr,
        "total_comparisons": total_comparisons[0],
        "steps": steps[:5]
    }


# ── Comparator key functions ────────────────────────────────────────

def best_price_key(product):
    """Minimum effective price across all available platforms."""
    prices = [
        p["price"] + p["deliveryCost"]
        for p in product["platforms"].values()
        if p["available"]
    ]
    return min(prices) if prices else float("inf")


def platform_price_key(platform):
    """Price on a specific platform."""
    def key_fn(product):
        p = product["platforms"].get(platform, {})
        if p.get("available"):
            return p["price"] + p["deliveryCost"]
        return float("inf")
    return key_fn


def rating_key(product):
    return -product["rating"]   # negate for descending


def review_count_key(product):
    return -product["reviewCount"]


def relevance_key(product):
    # Weighted: rating × log10(reviewCount)
    score = product["rating"] * math.log10(product["reviewCount"] + 1)
    return -score   # negate for descending
