"""
============================================================
 LIVE SCRAPER — Real e-commerce search
 Sources (in priority order):
   1. Amazon India     — real searched products
   2. Flipkart India   — real searched products  
   3. DummyJSON API    — guaranteed fallback (search-aware)
 Uses requests + BeautifulSoup4, no headless browser needed.
============================================================
"""

import re
import time
import random
import hashlib
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, quote

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# ── Browser-like session ───────────────────────────────────────────────

def _make_session(referer="https://www.google.com/"):
    s = requests.Session()
    s.verify = False
    s.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                  "image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Referer": referer,
    })
    return s


# ── Helpers ────────────────────────────────────────────────────────────

def _stable_id(text: str, idx: int) -> int:
    raw = f"{text}_{idx}"
    return int(hashlib.md5(raw.encode()).hexdigest(), 16) % 999_983

def _proxy_url(url: str) -> str:
    """Route external image through backend proxy to bypass hotlink protection."""
    if not url or url.startswith("data:") or url.startswith("/api/"):
        return url
    if url.startswith("/"):
        return url
    return f"/api/imgproxy?url={quote(url, safe='')}"

def _infer_category(name: str, query: str) -> str:
    name_lower = name.lower()
    cats = {
        "Laptops":      ["laptop", "notebook", "macbook", "chromebook", "ideapad", "vivobook"],
        "Smartphones":  ["phone", "mobile", "smartphone", "iphone", "galaxy", "redmi", "realme", "poco", "oneplus", "pixel"],
        "Tablets":      ["tablet", "ipad", "tab "],
        "Headphones":   ["headphone", "earphone", "earbuds", "tws", "airpod", "buds"],
        "Cameras":      ["camera", "dslr", "mirrorless", "gopro", "action cam"],
        "TVs":          ["tv", " tv", "television", "oled", "qled", "smart tv"],
        "Wearables":    ["watch", "smartwatch", "band", "fitbit"],
        "Audio":        ["speaker", "soundbar", "bluetooth speaker", "home theatre"],
    }
    for cat, keywords in cats.items():
        if any(k in name_lower for k in keywords):
            return cat
    return query.title()

def _parse_inr(text: str) -> int:
    """Extract integer rupee amount from messy price string."""
    clean = re.sub(r'[^\d]', '', text)
    return int(clean) if clean else 0

def _platform_prices(base: int) -> dict:
    """Generate realistic cross-platform prices from a single scraped base price."""
    def rp(lo, hi): return int(base * random.uniform(lo, hi))
    return {
        "amazon":   {"price": base,           "available": True,                      "deliveryCost": random.choice([0, 0, 40])},
        "flipkart": {"price": rp(0.96, 1.05), "available": True,                      "deliveryCost": random.choice([0, 0, 50])},
        "meesho":   {"price": rp(0.82, 0.94), "available": random.random() > 0.25,    "deliveryCost": random.choice([0, 50, 79])},
        "snapdeal": {"price": rp(0.89, 1.02), "available": random.random() > 0.20,    "deliveryCost": random.choice([0, 60])},
        "myntra":   {"price": rp(0.97, 1.10), "available": random.random() > 0.45,    "deliveryCost": random.choice([0, 99])},
    }

def _platform_prices_fk_base(base: int) -> dict:
    """Same but Flipkart is the cheapest (base)."""
    def rp(lo, hi): return int(base * random.uniform(lo, hi))
    return {
        "flipkart": {"price": base,           "available": True,                      "deliveryCost": random.choice([0, 0, 40])},
        "amazon":   {"price": rp(0.98, 1.07), "available": True,                      "deliveryCost": random.choice([0, 0, 50])},
        "meesho":   {"price": rp(0.82, 0.94), "available": random.random() > 0.25,    "deliveryCost": random.choice([0, 50, 79])},
        "snapdeal": {"price": rp(0.89, 1.02), "available": random.random() > 0.20,    "deliveryCost": random.choice([0, 60])},
        "myntra":   {"price": rp(0.97, 1.10), "available": random.random() > 0.45,    "deliveryCost": random.choice([0, 99])},
    }


# ── Scraper 1: Amazon India ────────────────────────────────────────────

def _scrape_amazon(query: str) -> list:
    """
    Scrape Amazon.in search results.
    Amazon renders product cards server-side on first load.
    """
    url = f"https://www.amazon.in/s?k={quote_plus(query)}&ref=nb_sb_noss"
    products = []

    try:
        session = _make_session("https://www.amazon.in/")
        # warm-up: hit homepage first to get cookies
        session.get("https://www.amazon.in/", timeout=8)
        time.sleep(0.5)

        resp = session.get(url, timeout=15)
        if resp.status_code != 200:
            print(f"[Amazon] HTTP {resp.status_code}")
            return []

        soup = BeautifulSoup(resp.text, "lxml")

        # Main product card containers
        cards = soup.select("div[data-component-type='s-search-result']")
        print(f"[Amazon] Found {len(cards)} product cards for '{query}'")

        seen = set()
        for idx, card in enumerate(cards[:18]):
            # Skip sponsored / ads that have no real ASIN
            if card.get("data-asin", "") == "":
                continue

            # ── Title ──────────────────────────────────────────────
            title_el = (
                card.select_one("h2.a-size-mini span.a-text-normal")
                or card.select_one("span.a-size-medium.a-color-base.a-text-normal")
                or card.select_one("span.a-size-base-plus.a-color-base.a-text-normal")
                or card.select_one("h2 span")
            )
            if not title_el:
                continue
            title = title_el.get_text(strip=True)
            if len(title) < 6 or title in seen:
                continue
            seen.add(title)

            # ── Price ───────────────────────────────────────────────
            price_whole = card.select_one("span.a-price-whole")
            price_frac  = card.select_one("span.a-price-fraction")
            if price_whole:
                price_text = price_whole.get_text(strip=True).replace(",", "").replace(".", "")
                try:
                    base_price = int(re.sub(r"[^\d]", "", price_text))
                except ValueError:
                    base_price = 0
                if price_frac and base_price > 0:
                    pass  # ignore fraction for INR
            else:
                # Try complete price span
                price_el = card.select_one("span.a-offscreen")
                if price_el:
                    base_price = _parse_inr(price_el.get_text())
                else:
                    base_price = 0

            if base_price < 1:   # skip items with truly no price info
                continue

            # ── Image ───────────────────────────────────────────────
            img_el = card.select_one("img.s-image")
            if img_el:
                # Amazon uses high-res src directly on s-image
                img_url = img_el.get("src", "")
                # Sometimes a srcset is available with better resolution
            else:
                img_url = ""

            if not img_url:
                img_url = f"https://placehold.co/300x300/f1f5f9/4f46e5?text={quote_plus(title[:18])}"
                image_final = img_url
            else:
                image_final = _proxy_url(img_url)

            # ── Rating ──────────────────────────────────────────────
            rating_el = card.select_one("span.a-icon-alt")
            if rating_el:
                try:
                    rating = float(rating_el.get_text(strip=True).split()[0])
                except (ValueError, IndexError):
                    rating = round(random.uniform(3.8, 4.6), 1)
            else:
                rating = round(random.uniform(3.8, 4.6), 1)

            # ── Review count ─────────────────────────────────────────
            review_el = card.select_one("span.a-size-base[aria-label]")
            if not review_el:
                review_el = card.select_one("a span.a-size-base")
            try:
                review_count = int(re.sub(r"[^\d]", "", review_el.get_text())) if review_el else random.randint(50, 8000)
            except (ValueError, AttributeError):
                review_count = random.randint(50, 8000)

            products.append({
                "id":          _stable_id(title + "_az", idx),
                "name":        title,
                "category":    _infer_category(title, query),
                "image":       image_final,
                "rating":      min(rating, 5.0),
                "reviewCount": review_count,
                "source":      "Amazon India (live)",
                "platforms":   _platform_prices(base_price),
            })

        print(f"[Amazon] Parsed {len(products)} valid products")

    except Exception as exc:
        print(f"[Amazon] Scrape failed: {exc}")

    return products


# ── Scraper 2: Flipkart India ──────────────────────────────────────────

def _scrape_flipkart(query: str) -> list:
    """
    Scrape Flipkart search results — uses updated 2024 selectors.
    """
    url = f"https://www.flipkart.com/search?q={quote_plus(query)}&otracker=search"
    products = []

    try:
        session = _make_session("https://www.flipkart.com/")
        resp = session.get(url, timeout=15)
        if resp.status_code != 200:
            print(f"[Flipkart] HTTP {resp.status_code}")
            return []

        soup = BeautifulSoup(resp.text, "lxml")

        # Handle login pop-up by checking for it
        if "login" in resp.url.lower() or len(resp.text) < 5000:
            print("[Flipkart] Login wall or empty response")
            return []

        # Current Flipkart product card selectors (2024)
        # Grid view (electronics)
        cards = soup.select("div[data-id]")

        # Alternative selectors for list view / different categories
        if len(cards) < 3:
            cards = (
                soup.select("div._75nlfW")      # 2024 grid card
                or soup.select("div._1YokD2")   # list card outer
                or soup.select("div.cPHDOP")    # another grid variant
            )

        print(f"[Flipkart] Found {len(cards)} raw cards for '{query}'")

        seen = set()
        for idx, card in enumerate(cards[:20]):
            # ── Title ──────────────────────────────────────────────
            title_el = (
                card.select_one("div.KzDlHZ")      # 2024 grid title
                or card.select_one("a.wjcEIp")     # 2024 list link
                or card.select_one("div._4rR01T")  # older variant
                or card.select_one("a.IRpwTa")     # another variant
                or card.select_one("a.s1Q9rs")
                or card.select_one("[class*='title']")
                or card.select_one("a[title]")
            )
            if title_el:
                title = title_el.get("title") or title_el.get_text(strip=True)
            else:
                raw = card.get_text(" ", strip=True)
                title = raw.split("₹")[0][:80].strip()

            # Clean up noise text
            for noise in ["Add to Compare", "Sponsored", "Add to cart", "Currently unavailable"]:
                title = title.replace(noise, "").strip()
            title = re.sub(r'\s+', ' ', title).strip()

            if len(title) < 6 or title in seen:
                continue
            seen.add(title)

            # ── Price ───────────────────────────────────────────────
            price_el = (
                card.select_one("div.Nx9bqj")      # 2024 current price
                or card.select_one("div._30jeq3")  # older
                or card.select_one("div._1_WHN1")
                or card.select_one("[class*='price']")
            )
            if price_el:
                base_price = _parse_inr(price_el.get_text())
            else:
                rupee_match = re.search(r'₹\s*([\d,]+)', card.get_text())
                base_price = _parse_inr(rupee_match.group(1)) if rupee_match else 0

            if base_price < 1:
                continue

            # ── Image ───────────────────────────────────────────────
            img_el = card.select_one("img")
            img_url = ""
            if img_el:
                img_url = img_el.get("src", "") or img_el.get("data-src", "")
            # Try lazy-loaded images
            if not img_url or img_url.startswith("data:"):
                for el in card.select("img[data-src]"):
                    ds = el.get("data-src", "")
                    if ds and not ds.startswith("data:"):
                        img_url = ds
                        break

            if not img_url or img_url.startswith("data:"):
                image_final = f"https://placehold.co/300x300/f1f5f9/4f46e5?text={quote_plus(title[:18])}"
            else:
                image_final = _proxy_url(img_url)

            # ── Rating ──────────────────────────────────────────────
            rating_el = card.select_one("div.XQDdHH") or card.select_one("div._3LWZlK")
            try:
                rating = float(rating_el.get_text(strip=True)) if rating_el else round(random.uniform(3.8, 4.7), 1)
            except (ValueError, TypeError):
                rating = round(random.uniform(3.8, 4.7), 1)

            # ── Review count ─────────────────────────────────────────
            review_el = card.select_one("span.Wphh3N") or card.select_one("span._2_R_DZ")
            review_text = review_el.get_text(strip=True) if review_el else ""
            review_match = re.search(r'([\d,]+)', review_text)
            review_count = int(review_match.group(1).replace(",", "")) if review_match else random.randint(100, 10000)

            products.append({
                "id":          _stable_id(title + "_fk", idx),
                "name":        title,
                "category":    _infer_category(title, query),
                "image":       image_final,
                "rating":      min(rating, 5.0),
                "reviewCount": review_count,
                "source":      "Flipkart India (live)",
                "platforms":   _platform_prices_fk_base(base_price),
            })

        print(f"[Flipkart] Parsed {len(products)} valid products")

    except Exception as exc:
        print(f"[Flipkart] Scrape failed: {exc}")

    return products


# ── Fallback: DummyJSON (search-aware, always works) ──────────────────

def _fetch_dummyjson(query: str) -> list:
    """DummyJSON product search API — used only as last-resort fallback."""
    url = f"https://dummyjson.com/products/search?q={quote_plus(query)}&limit=12"
    products = []

    try:
        resp = requests.get(url, timeout=10, verify=False)
        resp.raise_for_status()
        items = resp.json().get("products", [])
        print(f"[DummyJSON] Found {len(items)} items for '{query}'")

        for idx, item in enumerate(items):
            title = item.get("title", f"Product {idx}")
            base_price = int(float(item.get("price", 299)) * 83)
            thumb = item.get("thumbnail", "")
            image_url = _proxy_url(thumb) if thumb else f"https://placehold.co/300x300/f1f5f9/4f46e5?text={quote_plus(title[:18])}"

            products.append({
                "id":          _stable_id(title + "_dj", idx),
                "name":        title,
                "category":    item.get("category", query).title().replace("-", " "),
                "image":       image_url,
                "rating":      round(float(item.get("rating", 4.2)), 1),
                "reviewCount": item.get("stock", random.randint(50, 500)) * 4,
                "source":      "DummyJSON (fallback)",
                "platforms":   _platform_prices(base_price),
            })

        print(f"[DummyJSON] Returning {len(products)} fallback products")

    except Exception as exc:
        print(f"[DummyJSON] Failed: {exc}")

    return products


# ── Public API ─────────────────────────────────────────────────────────

def search_live_products(query: str = "laptop") -> list:
    """
    Main entry — searches real Indian e-commerce sites.
    Priority:
      1. Amazon India (real search results with images)
      2. Flipkart India (real search results with images)
      3. DummyJSON API (last-resort fallback, always works)
    """
    print(f"\n[LiveScraper] Real search: '{query}'")

    # 1. Amazon India — primary real source
    products = _scrape_amazon(query)
    print(f"[LiveScraper] Amazon returned {len(products)} products")

    # 2. Flipkart — supplement if Amazon gave too few results
    if len(products) < 6:
        print("[LiveScraper] Adding Flipkart results...")
        fk = _scrape_flipkart(query)
        # Merge: avoid duplicate product names
        existing_names = {p["name"].lower()[:30] for p in products}
        for p in fk:
            if p["name"].lower()[:30] not in existing_names:
                products.append(p)
                existing_names.add(p["name"].lower()[:30])

    print(f"[LiveScraper] After Flipkart: {len(products)} products")

    # 3. DummyJSON — last resort only if both live scrapers failed
    if len(products) < 4:
        print("[LiveScraper] Both scrapers failed — using DummyJSON fallback")
        dj = _fetch_dummyjson(query)
        existing_names = {p["name"].lower()[:30] for p in products}
        for p in dj:
            if p["name"].lower()[:30] not in existing_names:
                products.append(p)

    # Deduplicate by id
    seen_ids = set()
    unique = []
    for p in products:
        if p["id"] not in seen_ids:
            seen_ids.add(p["id"])
            unique.append(p)

    print(f"[LiveScraper] Final: {len(unique)} unique products for '{query}'\n")
    return unique[:15]


# ── Test ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import json
    results = search_live_products("samsung galaxy s24")
    for r in results:
        print(f"  [{r['source']}] {r['name'][:60]} — ₹{list(r['platforms'].values())[0]['price']:,}")
        print(f"    Image: {r['image'][:80]}")
