# 🛒 Smart Shopping Cart Optimizer (SSCO)

A full-stack application demonstrating practical implementations of **Design and Analysis of Algorithms (DAA)**. The platform scrapes real-time ecommerce catalog data via headless browser automation and applies algorithmic optimization techniques to solve budget allocation, product ranking, and delivery routing problems.

## ⚡ Algorithmic Implementations (DAA)

- **Greedy Strategy (0/1 & Fractional Knapsack):** Solves the constrained budget cart optimization problem to maximize product utility within user price caps.
- **Divide & Conquer (Merge Sort - O(n log n)):** High-throughput sorting and multi-attribute ranking across scraped price and rating matrices.
- **Graph Optimization (TSP & Kruskal's MST):** Route and delivery sequence optimization for multi-vendor fulfillment models.
- **Live Headless Automation:** Real-time product scraping across Amazon, Flipkart, Myntra, Snapdeal, and Meesho via Playwright.

## 🛠️ Technology Stack

- **Frontend:** Vanilla JavaScript (ES6+), Modern CSS3 Glassmorphism UI
- **Backend:** Python native `http.server` & standard library REST router
- **Automation Engine:** Microsoft Playwright (Headless Chromium)
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
