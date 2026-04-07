# Smart Shopping Cart Optimizer (SSCO) - Project Report

## 1. Title

**Smart Shopping Cart Optimizer (SSCO)**  
Design and Analysis of Algorithms (DAA) Based Shopping Price Comparison and Cart Optimization System

## 2. Abstract

Smart Shopping Cart Optimizer is a web-based application designed to compare products across multiple e-commerce platforms and optimize a user's shopping cart using core Design and Analysis of Algorithms concepts. The system demonstrates practical use of Merge Sort, Greedy algorithms, Fractional Knapsack, Traveling Salesman Problem using Dynamic Programming, and Kruskal's Minimum Spanning Tree algorithm.

The project includes a Python backend server, a vanilla HTML/CSS/JavaScript frontend, a sample product dataset, and a Playwright-based live product scraper. Users can browse products, filter and sort results, add items to cart, compare products, and run algorithmic optimization to reduce total cost and analyze platform ordering or delivery logistics.

## 3. Problem Statement

Online shoppers often compare prices manually across many e-commerce platforms before purchasing. This process is time-consuming and inefficient, especially when multiple products are involved. The problem becomes more complex when users need to consider platform availability, delivery cost, budget constraints, and ordering strategy.

This project solves the problem by building a shopping optimizer that:

- Displays products from multiple platforms.
- Finds the best platform for each item.
- Sorts products using a manual algorithmic implementation.
- Optimizes cart cost using Greedy logic.
- Supports budget-based product selection using Fractional Knapsack.
- Demonstrates platform order optimization using TSP.
- Demonstrates logistics network optimization using MST.

## 4. Objectives

- Build a functional shopping cart optimization system.
- Apply DAA algorithms in a real-world shopping scenario.
- Compare effective product prices including delivery cost.
- Provide an interactive frontend for browsing, cart management, comparison, and algorithm visualization.
- Implement a Python backend using REST-style API endpoints.
- Demonstrate algorithm complexity and intermediate steps to support academic explanation.
- Support live product lookup through Playwright scraping with fallback sample data.

## 5. Technology Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Backend | Python `http.server`, `ThreadingHTTPServer` |
| Data Format | JSON |
| Scraping | Playwright Python |
| Deployment | Docker with Microsoft Playwright Python image |
| Storage | Browser `localStorage` for cart and compare state |
| Version Control | Git |

## 6. Project Structure

The current working copy uses a root-level layout:

```text
SSCO/
  index.html
  products.html
  cart.html
  compare.html
  algorithms.html
  style.css
  state.js
  server.py
  products.py
  live_scraper.py
  merge_sort.py
  greedy.py
  tsp.py
  mst.py
  test_scraper.py
  Dockerfile
  requirements.txt
  amazon.html
```

Important note: The Git-tracked repository appears to originally use `backend/` and `frontend/` folders, while the current working tree has many files flattened into the root directory. If deploying or committing, the layout should be cleaned up so the Dockerfile and repository structure match.

## 7. System Architecture

The project follows a simple client-server architecture.

```text
User Browser
    |
    | HTML/CSS/JS pages
    v
Frontend UI
    |
    | fetch() API calls
    v
Python Backend Server
    |
    | imports product data and algorithm modules
    v
Algorithm Layer + Product Dataset + Live Scraper
```

The frontend handles user interaction, product cards, cart state, comparison state, and displaying algorithm results. The backend exposes API endpoints and coordinates product retrieval, sorting, optimization, and algorithm output generation.

## 8. Major Modules

### 8.1 `server.py`

`server.py` is the main backend file. It uses Python's `ThreadingHTTPServer` and `SimpleHTTPRequestHandler` to serve both static frontend files and API endpoints.

Main responsibilities:

- Serve frontend files such as `index.html`, `products.html`, and `cart.html`.
- Provide API routes for products, categories, algorithms, and optimization.
- Maintain in-memory product cache for live scraped products.
- Run cart optimization by coordinating Greedy, TSP, MST, Knapsack, and Merge Sort modules.
- Read the deployment port from the `PORT` environment variable.

Important routes:

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/health` | GET | Server health check |
| `/api/products` | GET | Product listing with sorting/filtering |
| `/api/products/<id>` | GET | Product lookup by ID |
| `/api/categories` | GET | Product category list |
| `/api/algorithms` | GET | Algorithm metadata |
| `/api/optimize` | POST | Full cart optimization |
| `/api/optimize/greedy` | POST | Greedy-only optimization |
| `/api/optimize/knapsack` | POST | Budget optimization |
| `/api/optimize/mst` | GET | MST demonstration |

### 8.2 `products.py`

`products.py` contains the sample product dataset. Each product includes:

- Product ID
- Product name
- Category
- Image URL
- Description
- Rating and review count
- Specifications
- Platform-wise price, delivery days, delivery cost, and availability
- Price history

It also contains platform metadata for Amazon, Flipkart, Meesho, Snapdeal, and Myntra.

### 8.3 `live_scraper.py`

`live_scraper.py` uses Playwright to search Flipkart for live products. It launches Chromium in headless mode with Docker-friendly browser flags.

Main responsibilities:

- Search Flipkart using a query string.
- Extract product-like blocks from the live search page.
- Extract title, price, and image when available.
- Generate a platform-wise price structure compatible with the rest of the app.

Limitation: The current scraper pulls base product data from Flipkart and then simulates some platform prices, availability, ratings, and review counts using random values. Therefore, it should be described as "live product discovery with simulated cross-platform comparison" unless all platform data is implemented through real scraping or official APIs.

### 8.4 `merge_sort.py`

This module implements Merge Sort manually without using Python's built-in sorting for main product display sorting.

Use cases:

- Sort products by best price.
- Sort by specific platform price.
- Sort by rating.
- Sort by review count.
- Sort by relevance.

Complexity:

- Time Complexity: `O(n log n)`
- Space Complexity: `O(n)`

### 8.5 `greedy.py`

This module implements two Greedy-based algorithms.

`greedy_cheapest_platform(cart_items)`:

- Scans every available platform for each product.
- Selects the platform with the minimum effective cost.
- Effective cost is `price + deliveryCost`.
- Calculates total optimized cost and savings compared with a naive Amazon baseline.

Complexity:

- Time Complexity: `O(n x P)`, where `n` is number of cart items and `P` is number of platforms.
- Space Complexity: `O(n)`

`fractional_knapsack(products, budget)`:

- Computes a value score based on rating and review count.
- Calculates value-to-price ratio.
- Selects full or fractional products within budget.

Complexity:

- Time Complexity: `O(n log n)`
- Space Complexity: `O(n)`

### 8.6 `tsp.py`

This module implements platform order optimization using the Held-Karp Dynamic Programming solution for the Traveling Salesman Problem.

In this project:

- Platforms are treated like cities.
- Edge weights represent transition or logistics overhead between platforms.
- The algorithm determines an efficient ordering of active platforms used by cart items.

Complexity:

- Time Complexity: `O(2^P x P^2)`
- Space Complexity: `O(2^P x P)`

Since the number of platforms is small, this exact DP method is practical for the project.

### 8.7 `mst.py`

This module implements Kruskal's Minimum Spanning Tree algorithm using Union-Find / Disjoint Set Union.

In this project:

- Platforms are graph nodes.
- Edges represent logistics cost between platforms.
- MST finds a minimum-cost network connecting active platforms.

Complexity:

- Time Complexity: `O(E log E)`
- Space Complexity: `O(V + E)`

### 8.8 `state.js`

`state.js` contains shared frontend logic.

Main responsibilities:

- Store cart items in `localStorage`.
- Store compare items in `localStorage`.
- Render navbar and badges.
- Render product cards.
- Format prices.
- Render star ratings and sparklines.
- Handle add/remove cart and compare actions.

### 8.9 Frontend HTML Pages

| File | Purpose |
|---|---|
| `index.html` | Landing page with search, feature highlights, and algorithm overview |
| `products.html` | Product browsing, sorting, platform filtering, category filtering |
| `cart.html` | Cart display and optimization result visualization |
| `compare.html` | Product comparison and price history chart |
| `algorithms.html` | Algorithm reference and interactive demonstrations |

### 8.10 `style.css`

`style.css` provides the complete visual design of the app, including:

- Light glassmorphism theme
- Navbar
- Product cards
- Buttons and badges
- Algorithm result accordions
- Tables
- Toast messages
- Responsive layouts

## 9. Algorithm Explanation

### 9.1 Merge Sort

Merge Sort is used for sorting product lists. It follows the Divide and Conquer strategy.

Steps:

1. Divide the product list into two halves.
2. Recursively sort both halves.
3. Merge the sorted halves.

Why it is used:

- Stable and predictable `O(n log n)` performance.
- Demonstrates Divide and Conquer clearly.
- Useful for sorting by price, rating, review count, or relevance.

### 9.2 Greedy Cheapest Platform Selection

For each product in the cart, the algorithm chooses the platform with the lowest effective cost.

Formula:

```text
effective_cost = product_price + delivery_cost
```

Why Greedy works here:

- Each product decision is independent.
- There is no constraint requiring all items to be bought from the same platform.
- A local minimum for each item contributes to the global minimum total cost.

### 9.3 Fractional Knapsack

Fractional Knapsack is used for budget-constrained selection. Products are assigned a value score based on rating and review count. The algorithm chooses products by highest value-to-price ratio.

Formula:

```text
ratio = value / price
```

Why it is used:

- Demonstrates a classic Greedy algorithm.
- Shows how to maximize value under a budget.
- Supports fractional selection for academic demonstration.

### 9.4 Held-Karp TSP

Held-Karp TSP is used to decide the best order of platforms used in the cart.

Why it is used:

- Demonstrates Dynamic Programming with bitmasking.
- Useful for modeling platform transition overhead.
- Works well because the number of platforms is small.

### 9.5 Kruskal's MST

Kruskal's MST builds a minimum-cost network connecting platforms.

Steps:

1. Generate all platform-to-platform edges.
2. Sort edges by weight.
3. Add the smallest edge that does not form a cycle.
4. Use Union-Find to detect cycles.
5. Stop when `V - 1` edges are selected.

Why it is used:

- Demonstrates Graph Algorithms.
- Shows minimum logistics network construction.
- Provides clear accepted/rejected edge visualization.

## 10. Application Workflow

1. User opens the home page.
2. User searches for products or navigates to the products page.
3. Frontend calls `/api/products`.
4. Backend retrieves live scraped products or falls back to sample products.
5. Backend sorts products using Merge Sort.
6. User adds products to cart or comparison list.
7. Cart and compare state are stored in browser `localStorage`.
8. User runs cart optimization from the cart page.
9. Frontend sends selected product IDs and optional budget to `/api/optimize`.
10. Backend runs Greedy platform selection, TSP, MST, Knapsack, and Merge Sort.
11. Frontend displays savings, selected platforms, algorithm steps, and complexity analysis.

## 11. Testing and Verification

The following checks were performed during repository analysis:

- Python syntax compilation passed for:
  - `server.py`
  - `live_scraper.py`
  - `products.py`
  - `merge_sort.py`
  - `greedy.py`
  - `tsp.py`
  - `mst.py`
  - `test_scraper.py`

- Runtime smoke test passed:
  - Imported `server.py`.
  - Ran `optimize_cart(PRODUCTS[:3], budget=100000)`.
  - Received a successful optimization result.

- Dependency import check passed in the current environment:
  - `playwright.sync_api`
  - `requests`
  - `bs4`

Note: `requests` and `beautifulsoup4` are used by `test_scraper.py` but are not listed in `requirements.txt`. They may fail in a fresh environment unless added.

## 12. Strengths

- Demonstrates multiple DAA algorithms in one practical project.
- Provides interactive frontend visualization.
- Uses manual Merge Sort for product sorting.
- Shows algorithm complexity and step-by-step results.
- Uses simple Python backend without heavyweight web frameworks.
- Supports Docker-based deployment for Playwright compatibility.
- Maintains cart and compare state in browser storage.

## 13. Limitations

- Current working tree layout does not match the Git-tracked `backend/` and `frontend/` layout.
- Dockerfile still expects `/app/backend`, which conflicts with the current root-level `server.py`.
- Cross-platform live pricing is partially simulated.
- Live scraper depends on Flipkart page structure, which may change.
- Product IDs generated with Python `hash()` are not stable across server restarts.
- Some frontend HTML is built with `innerHTML` using product data, so external product fields should be escaped.
- `.pyc` files and `__pycache__` artifacts are present and should usually be ignored.
- `amazon.html` is a large scraped page artifact and should be separated from app source if not required at runtime.

## 14. Future Scope

- Restore or standardize project layout into a clean `backend/` and `frontend/` structure.
- Update Dockerfile to match the final layout.
- Add `.gitignore` for generated files.
- Replace random simulated prices with real API or multi-platform scraping data.
- Use deterministic product IDs, such as SHA-256 based IDs.
- Add frontend escaping utilities or DOM-based rendering for product data.
- Add automated unit tests for all algorithms.
- Add API-level tests for backend routes.
- Add loading/error states for scraper failures.
- Add persistent backend storage for carts and search results.
- Add user accounts and saved carts.
- Add price tracking alerts.

## 15. Conclusion

Smart Shopping Cart Optimizer successfully demonstrates how core DAA concepts can be applied to a real-world shopping optimization problem. The project combines product comparison, cart optimization, sorting, budget selection, graph algorithms, and dynamic programming into one interactive system.

The project is suitable for academic DAA demonstration because each algorithm has a clear role:

- Merge Sort for product sorting.
- Greedy selection for lowest-cost platform choice.
- Fractional Knapsack for budget optimization.
- Held-Karp TSP for platform order optimization.
- Kruskal's MST for logistics network optimization.

With cleanup of repository structure, deployment configuration, and scraper reliability, the project can be made more production-ready while preserving its educational algorithm-focused purpose.
