/**
 * Shared state management using localStorage
 * Cart and Compare feature state
 */
const STATE = {
  // ── Cart ────────────────────────────────────────────────
  getCart() {
    try { return JSON.parse(localStorage.getItem('ssco_cart') || '[]'); }
    catch { return []; }
  },
  saveCart(items) {
    localStorage.setItem('ssco_cart', JSON.stringify(items));
    this._notify('cart');
  },
  addToCart(product) {
    const cart = this.getCart();
    if (!cart.find(p => p.id === product.id)) {
      cart.push(product);
      this.saveCart(cart);
      showToast(`Added "${product.name.slice(0,20)}..." to cart 🛒`, 'success');
    } else {
      showToast('Already in cart!', 'info');
    }
  },
  removeFromCart(productId) {
    const cart = this.getCart().filter(p => p.id !== productId);
    this.saveCart(cart);
  },
  clearCart() { this.saveCart([]); },
  isInCart(productId) { return this.getCart().some(p => p.id === productId); },
  cartCount() { return this.getCart().length; },

  // ── Compare ─────────────────────────────────────────────
  getCompare() {
    try { return JSON.parse(localStorage.getItem('ssco_compare') || '[]'); }
    catch { return []; }
  },
  saveCompare(items) {
    localStorage.setItem('ssco_compare', JSON.stringify(items));
    this._notify('compare');
  },
  addToCompare(product) {
    const list = this.getCompare();
    if (list.find(p => p.id === product.id)) {
      showToast('Already in compare list!', 'info'); return;
    }
    if (list.length >= 3) list.shift(); // keep max 3
    list.push(product);
    this.saveCompare(list);
    showToast(`Added to compare ⚖️`, 'info');
  },
  removeFromCompare(productId) {
    this.saveCompare(this.getCompare().filter(p => p.id !== productId));
  },
  isInCompare(productId) { return this.getCompare().some(p => p.id === productId); },
  compareCount() { return this.getCompare().length; },

  // ── Listeners ────────────────────────────────────────────
  _listeners: {},
  on(event, fn) {
    if (!this._listeners[event]) this._listeners[event] = [];
    this._listeners[event].push(fn);
  },
  _notify(event) {
    (this._listeners[event] || []).forEach(fn => fn());
  }
};

// ── Toast System ──────────────────────────────────────────
let _toastWrap = null;
function getToastWrap() {
  if (!_toastWrap) {
    _toastWrap = document.createElement('div');
    _toastWrap.className = 'toast-wrap';
    document.body.appendChild(_toastWrap);
  }
  return _toastWrap;
}
function showToast(msg, type = 'info', duration = 2800) {
  const wrap = getToastWrap();
  const t = document.createElement('div');
  t.className = `toast toast-${type}`;
  t.textContent = msg;
  wrap.appendChild(t);
  setTimeout(() => {
    t.style.opacity = '0';
    t.style.transition = 'opacity .3s';
    setTimeout(() => wrap.removeChild(t), 300);
  }, duration);
}

// ── Navbar badge updater ──────────────────────────────────
function updateNavBadges() {
  const cartBadge    = document.getElementById('cart-badge');
  const compareBadge = document.getElementById('compare-badge');
  if (cartBadge)    cartBadge.textContent    = STATE.cartCount() || '';
  if (compareBadge) compareBadge.textContent = STATE.compareCount() || '';
}

// ── Navbar HTML injector ──────────────────────────────────
function renderNavbar(activePage) {
  const pages = [
    { href:'/',             label:'Home',      icon:'🏠', page:'home' },
    { href:'/products',     label:'Products',  icon:'📦', page:'products', id:'nav-products' },
    { href:'/compare',      label:'Compare',   icon:'⚖️', page:'compare',  badge:'compare-badge' },
    { href:'/cart',         label:'Cart',      icon:'🛒', page:'cart',     badge:'cart-badge' },
    { href:'/algorithms',   label:'DAA Info',  icon:'🧠', page:'algorithms' }
  ];
  const nav = document.getElementById('navbar');
  if (!nav) return;

  nav.innerHTML = `
    <div class="nav-inner">
      <a href="/" class="nav-logo">
        <div class="nav-logo-icon">🛒</div>
        <div class="nav-logo-text">
          <span>SSCO</span>
          <span>SMART CART OPTIMIZER</span>
        </div>
      </a>
      <nav class="nav-links">
        ${pages.map(p => `
          <a href="${p.href}" class="nav-link${p.page === activePage ? ' active' : ''}"
             ${p.id ? `id="${p.id}"` : ''}>
            <span>${p.icon}</span>
            <span>${p.label}</span>
            ${p.badge ? `<span class="nav-badge" id="${p.badge}"></span>` : ''}
          </a>
        `).join('')}
      </nav>
    </div>`;

  updateNavBadges();
  STATE.on('cart',    updateNavBadges);
  STATE.on('compare', updateNavBadges);
}

// ── Stars renderer ────────────────────────────────────────
function starHTML(rating) {
  const full = Math.floor(rating);
  const half = rating % 1 >= 0.5 ? '½' : '';
  const empty = 5 - full - (half ? 1 : 0);
  return `<span class="stars">${'★'.repeat(full)}${half}${'☆'.repeat(empty)}</span>`;
}

// ── Price formatter ───────────────────────────────────────
function fmtPrice(n) {
  return '₹' + Number(n).toLocaleString('en-IN');
}

function escapeHTML(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function safeProductImage(value) {
  const url = String(value ?? '');
  if (/^https?:\/\//i.test(url) || url.startsWith('data:image/')) {
    return escapeHTML(url);
  }
  return 'https://placehold.co/400x400';
}

// ── Platform display info ─────────────────────────────────
const PLAT = {
  amazon:   { label:'Amazon',   color:'#FF9900', cls:'amazon'   },
  flipkart: { label:'Flipkart', color:'#2874F0', cls:'flipkart' },
  meesho:   { label:'Meesho',  color:'#f43f5e', cls:'meesho'   },
  snapdeal: { label:'Snapdeal', color:'#e4142c', cls:'snapdeal' },
  myntra:   { label:'Myntra',  color:'#ff3f6c', cls:'myntra'   }
};

// ── Display Price across platforms ──────────────────────────
function getDisplayPrice(product, platformContext = null) {
  if (platformContext && product.platforms[platformContext] && product.platforms[platformContext].available) {
    const p = product.platforms[platformContext];
    return { price: p.price + p.deliveryCost, platform: platformContext };
  }

  let best = Infinity, bestPlatform = null;
  for (const [name, p] of Object.entries(product.platforms)) {
    if (p.available) {
      const eff = p.price + p.deliveryCost;
      if (eff < best) { best = eff; bestPlatform = name; }
    }
  }
  return { price: best, platform: bestPlatform };
}

const getBestPrice = getDisplayPrice;

// ── Product Card HTML ─────────────────────────────────────
function productCardHTML(product, platformContext = null) {
  const { price: displayPrice, platform: displayPlatform } = getDisplayPrice(product, platformContext);
  const pi = PLAT[displayPlatform] || {};
  const inCart    = STATE.isInCart(product.id);
  const inCompare = STATE.isInCompare(product.id);
  const amazonP   = product.platforms.amazon;
  const amazonEff = amazonP?.available ? amazonP.price + amazonP.deliveryCost : null;
  const savings   = amazonEff && amazonEff > displayPrice ? amazonEff - displayPrice : 0;
  const productName = escapeHTML(product.name);
  const productCategory = escapeHTML(product.category);
  const productImage = safeProductImage(product.image);
  const fallbackText = encodeURIComponent(String(product.name ?? '').slice(0, 6));
  const productId = Number.parseInt(product.id, 10) || 0;

  const availPlatforms = Object.entries(product.platforms)
    .filter(([, p]) => p.available)
    .map(([name, p]) => {
      const pl = PLAT[name] || {};
      const eff = p.price + (p.deliveryCost || 0);
      return `<span class="prod-plat-pill badge-${pl.cls}"
        title="${pl.label}: ${fmtPrice(p.price)} + ₹${p.deliveryCost||0} delivery"
        style="color:${pl.color};border-color:${pl.color}35;background:${pl.color}12">
        <span style="font-size:.65rem;opacity:.8">${pl.label}</span>
        <span style="font-weight:700">${fmtPrice(p.price)}</span>
      </span>`;
    }).join('');
  // When no platform selected, show best deal platform badge
  const badgePlatform = displayPlatform || 'flipkart';
  const badgePi = PLAT[badgePlatform] || {};
  const badgeLabel = platformContext ? badgePi.label : `Best: ${badgePi.label}`;
  <div class="card prod-card fade-in" data-id="${productId}">
    <div class="prod-thumb">
      <img src="${productImage}" alt="${productName}"
           onerror="this.src='https://placehold.co/200x140/1a1a35/6366f1?text=${fallbackText}'" />
      <div class="prod-plat-badge badge-${pi.cls}"
           style="color:${pi.color};border-color:${pi.color}40;background:${pi.color}18">
        ${pi.label}
      </div>
      <button class="prod-compare-btn ${inCompare ? 'active' : ''}"
              onclick="toggleCompare(${productId})" title="Compare">
        ${inCompare ? '✓ Compare' : '⚖️ Compare'}
      </button>
      ${savings > 0 ? `<div class="prod-save">Save ${fmtPrice(savings)}</div>` : ''}
    </div>
    <div class="prod-body">
      <div class="prod-cat">${productCategory}</div>
      <a href="/products#${productId}" class="prod-name">${productName}</a>
      <div style="display:flex;align-items:center;gap:.5rem">
        ${starHTML(product.rating)}
        <span style="font-size:.76rem;color:var(--text-3)">
          ${product.rating} (${product.reviewCount.toLocaleString('en-IN')})
        </span>
      </div>
      <div>
        <span class="prod-price">${fmtPrice(displayPrice)}</span>
        ${amazonEff && amazonEff > displayPrice ? `<span class="prod-price-old">${fmtPrice(amazonEff)}</span>` : ''}
      </div>
      <div class="prod-plats">${availPlatforms}</div>
      <div class="algo-tag algo-dc" style="width:fit-content;margin-top:.2rem;font-size:.62rem">
        📊 Merge Sort O(n log n)
      </div>
      <div class="prod-actions">
        <button class="btn ${inCart ? 'btn-ghost' : 'btn-primary'}"
                onclick="toggleCart(${productId})">
          ${inCart ? '✓ In Cart' : '🛒 Add to Cart'}
        </button>
        <a href="/products#detail-${productId}" class="prod-view-btn">👁️</a>
      </div>
    </div>
  </div>`;
}

// ── Global toggle functions (called from inline onclick) ──
function toggleCart(productId) {
  if (STATE.isInCart(productId)) {
    STATE.removeFromCart(productId);
  } else {
    // Fetch product from cache or API
    const cards = document.querySelectorAll(`[data-id="${productId}"]`);
    if (_productCache[productId]) {
      STATE.addToCart(_productCache[productId]);
    } else {
      fetch(`/api/products/${productId}`)
        .then(r => r.json())
        .then(d => { STATE.addToCart(d.product); })
        .catch(() => showToast('Error adding to cart', 'error'));
    }
  }
  // Update all matching cards' buttons on page
  document.querySelectorAll(`[data-id="${productId}"] .btn`).forEach(btn => {
    const inCart = STATE.isInCart(productId);
    btn.className = `btn ${inCart ? 'btn-ghost' : 'btn-primary'}`;
    btn.textContent = inCart ? '✓ In Cart' : '🛒 Add to Cart';
  });
}

function toggleCompare(productId) {
  if (STATE.isInCompare(productId)) {
    STATE.removeFromCompare(productId);
  } else {
    if (_productCache[productId]) {
      STATE.addToCompare(_productCache[productId]);
    } else {
      fetch(`/api/products/${productId}`)
        .then(r => r.json())
        .then(d => { STATE.addToCompare(d.product); })
        .catch(() => showToast('Error', 'error'));
    }
  }
  document.querySelectorAll(`[data-id="${productId}"] .prod-compare-btn`).forEach(btn => {
    const inCmp = STATE.isInCompare(productId);
    btn.className = `prod-compare-btn ${inCmp ? 'active' : ''}`;
    btn.textContent = inCmp ? '✓ Compare' : '⚖️ Compare';
  });
}

// Product cache to avoid extra API calls
const _productCache = {};

// ── Sparkline SVG from price history ─────────────────────
function sparklineHTML(history) {
  if (!history || history.length < 2) return '';
  const min = Math.min(...history);
  const max = Math.max(...history);
  const w = 200, h = 55;
  const pts = history.map((v, i) => {
    const x = (i / (history.length - 1)) * w;
    const y = h - ((v - min) / (max - min || 1)) * (h - 6) - 3;
    return `${x.toFixed(1)},${y.toFixed(1)}`;
  }).join(' ');
  return `<svg viewBox="0 0 ${w} ${h}" xmlns="http://www.w3.org/2000/svg">
    <polyline points="${pts}" fill="none" stroke="#6366f1" stroke-width="2.5"
      stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="${(history.length-1)/(history.length-1)*w}" cy="${h-((history[history.length-1]-min)/(max-min||1))*(h-6)-3}" r="4" fill="#6366f1"/>
  </svg>`;
}
