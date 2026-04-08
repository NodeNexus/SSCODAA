# 🛒 Smart Shopping Cart Optimizer (DAA Project)

A sophisticated full-stack web application designed for analyzing and demonstrating **Design and Analysis of Algorithms (DAA)**. Live internet product data is dynamically scraped using a headless Chromium browser and sorted with deep DAA concepts.

## 🌟 Features
- **Live Headless Web Scraping:** Real-time data from platforms like Amazon, Flipkart, Myntra, Snapdeal, and Meesho.
- **Glassmorphism UI**: High-end light-theme user interface with frosty glass overlays, micro-animations, and dynamic background blobs.
- **DAA Implementations**:
  - **Divide & Conquer**: Merge Sort (O(n log n)) for lightning-fast live product sorting.
  - **Greedy Strategy**: Knapsack algorithms for budget optimization.
  - **Graph Algorithms**: Traveling Salesperson (TSP) & Kruskal's Minimum Spanning Tree (MST).
  
## 🛠️ Technology Stack
**Frontend:** Vanilla JS, DOM DOM Manipulation, Modern CSS3 (Glassmorphism & Keyframes).
**Backend:** Pure native Python `http.server` & standard libraries.
**Web Automation:** Microsoft Playwright (Python).
**Architecture:** RESTful GET/POST Routing API.

---

### Requirements
- Python 3.10+
- Playwright Chromium dependencies

### Installation Steps
1. Clone the repository: `git clone https://github.com/NodeNexus/SSCO.git`
2. Enter the repository root directory.
3. Install system requirements:
```bash
pip install -r requirements.txt
playwright install chromium
```
4. Run the Python backend server:
```bash
cd backend
python server.py
```
5. Open your web browser to **http://localhost:5000** 

---

This project is fully dockerized to bypass native web-server sandboxes and safely execute headless Chromium engines in isolated security containers.
