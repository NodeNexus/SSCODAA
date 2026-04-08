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

## 🚀 How to Run Locally

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

## ☁️ How to Deploy Online to Render

This project is fully dockerized to bypass native web-server sandboxes and safely execute headless Chromium engines in isolated security containers.

### Deployment Walkthrough
1. **Prepare Your GitHub:** Ensure this codebase (along with the `Dockerfile` and `requirements.txt`) is perfectly synced to your GitHub branch.
2. **Setup Render:** Navigate to the [Render Dashboard](https://dashboard.render.com).
3. **Launch Service:** Click **"New +"** and choose **"Web Service"**.
4. **Connect Repository:** Link your `NodeNexus/SSCO` GitHub repository.
5. **CRITICAL Configuration:**
   - Instead of Native Python, select **Docker** as your runtime/environment.
   - Leave build and start commands blank (Render auto-detects our `Dockerfile`).
6. **Launch:** Click **Deploy**. Render will fetch our system dependencies, install Playwright binaries, circumvent Sandbox restrictions, and dynamically map standard open host ports mapping your `server.py` daemon directly into the cloud.

Done! Give Render roughly 3 to 5 minutes to complete the image build. You'll receive a live URL (`https://your-app-name.onrender.com`)!
