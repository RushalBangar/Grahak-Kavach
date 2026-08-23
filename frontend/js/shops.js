/**
 * GRAHAK KAVACH — Shop Compliance History & Transparency Explorer
 */

const Shops = {
  init() {
    this.bindEvents();
    this.loadInitialShops();
  },

  bindEvents() {
    const searchInput = document.getElementById('shopSearchInput');
    const searchBtn = document.getElementById('shopSearchBtn');
    const addShopBtn = document.getElementById('addNewShopBtn');
    const addShopForm = document.getElementById('addShopForm');

    if (searchBtn && searchInput) {
      searchBtn.addEventListener('click', () => this.handleSearch(searchInput.value.trim()));
      searchInput.addEventListener('input', (e) => this.handleSearch(e.target.value.trim()));
    }

    if (addShopBtn) {
      addShopBtn.addEventListener('click', () => this.openAddShopModal());
    }

    if (addShopForm) {
      addShopForm.addEventListener('submit', (e) => this.handleAddShopSubmit(e));
    }
  },

  async loadInitialShops() {
    const listContainer = document.getElementById('shopSearchResultsList');
    if (!listContainer) return;

    listContainer.innerHTML = CONFIG.INITIAL_SHOPS.map((shop, index) => `
      <div class="shop-item-card ${index === 0 ? 'active' : ''}" onclick="Shops.selectShop(${shop.id}, this)">
        <h4 style="font-size: 0.95rem; margin-bottom: 0.2rem;">${shop.name}</h4>
        <p style="font-size: 0.8rem;"><i class="fas fa-map-marker-alt"></i> ${shop.address}</p>
      </div>
    `).join('');

    // Load first shop's history
    if (CONFIG.INITIAL_SHOPS.length > 0) {
      this.selectShop(CONFIG.INITIAL_SHOPS[0].id);
    }
  },

  async handleSearch(query) {
    const listContainer = document.getElementById('shopSearchResultsList');
    if (!listContainer) return;

    const shops = await API.searchShops(query || '');
    if (shops.length === 0) {
      listContainer.innerHTML = `<div style="padding: 1.5rem; text-align: center; color: var(--text-muted);">No shops found. You can add this shop below!</div>`;
      return;
    }

    listContainer.innerHTML = shops.map((shop, index) => `
      <div class="shop-item-card ${index === 0 ? 'active' : ''}" onclick="Shops.selectShop(${shop.id}, this)">
        <h4 style="font-size: 0.95rem; margin-bottom: 0.2rem;">${shop.name}</h4>
        <p style="font-size: 0.8rem;"><i class="fas fa-map-marker-alt"></i> ${shop.address}</p>
      </div>
    `).join('');
  },

  async selectShop(shopId, elementNode) {
    if (elementNode) {
      document.querySelectorAll('.shop-item-card').forEach(c => c.classList.remove('active'));
      elementNode.classList.add('active');
    }

    const historyContainer = document.getElementById('shopHistoryDetailsView');
    if (!historyContainer) return;

    try {
      const data = await API.getShopHistory(shopId);
      this.renderShopDetails(data);
    } catch (err) {
      App.showToast('Failed to load shop history', 'error');
    }
  },

  renderShopDetails(data) {
    const shop = data.shop || {};
    const inspections = data.inspections || [];
    const resolved = data.resolved_complaints || [];

    const passedCount = inspections.filter(i => i.is_compliant).length;
    const violationCount = inspections.filter(i => !i.is_compliant).length;
    const total = inspections.length || 1;
    const trustScore = Math.round((passedCount / total) * 100);

    const nameEl = document.getElementById('shopDetailName');
    const addrEl = document.getElementById('shopDetailAddress');
    const scoreCircle = document.getElementById('shopTrustScoreCircle');
    const inspectionsListEl = document.getElementById('shopInspectionsList');
    const complaintsListEl = document.getElementById('shopResolvedComplaintsList');

    if (nameEl) nameEl.innerText = shop.name;
    if (addrEl) addrEl.innerText = shop.address;

    if (scoreCircle) {
      scoreCircle.innerText = `${trustScore}%`;
      scoreCircle.style.borderColor = trustScore > 75 ? 'var(--accent-emerald)' : (trustScore > 50 ? 'var(--accent-amber)' : 'var(--accent-rose)');
      scoreCircle.style.color = scoreCircle.style.borderColor;
    }

    if (inspectionsListEl) {
      if (inspections.length === 0) {
        inspectionsListEl.innerHTML = `<p style="font-size: 0.85rem; color: var(--text-muted);">No official officer inspections recorded yet.</p>`;
      } else {
        inspectionsListEl.innerHTML = inspections.map(i => `
          <div style="padding: 0.75rem 0; border-bottom: 1px solid var(--border-subtle); display: flex; justify-content: space-between; align-items: center;">
            <div>
              <div style="font-size: 0.85rem; font-weight: 600;">${i.details || 'Routine Inspection'}</div>
              <div style="font-size: 0.75rem; color: var(--text-muted);">${new Date(i.date).toLocaleDateString()}</div>
            </div>
            <span class="status-tag ${i.is_compliant ? 'pass' : 'violation'}">
              <i class="fas ${i.is_compliant ? 'fa-check-circle' : 'fa-times-circle'}"></i> ${i.is_compliant ? 'Pass' : 'Violation'}
            </span>
          </div>
        `).join('');
      }
    }

    if (complaintsListEl) {
      if (resolved.length === 0) {
        complaintsListEl.innerHTML = `<p style="font-size: 0.85rem; color: var(--text-muted);">No resolved complaints on record.</p>`;
      } else {
        complaintsListEl.innerHTML = resolved.map(c => `
          <div style="padding: 0.65rem 0; border-bottom: 1px solid var(--border-subtle); font-size: 0.82rem; display: flex; justify-content: space-between;">
            <span><i class="fas fa-check text-gradient"></i> Docket #${c.tracking_id} (${c.violation_type})</span>
            <span style="color: var(--text-muted);">${new Date(c.date).toLocaleDateString()}</span>
          </div>
        `).join('');
      }
    }
  },

  openAddShopModal() {
    const modal = document.getElementById('addShopModal');
    if (modal) modal.classList.add('open');
  },

  async handleAddShopSubmit(e) {
    e.preventDefault();
    const name = document.getElementById('newShopName').value.trim();
    const address = document.getElementById('newShopAddress').value.trim();

    if (!name || !address) {
      App.showToast('Please fill all shop fields.', 'warning');
      return;
    }

    try {
      const newShop = await API.createShop({ name, address });
      App.showToast(`Shop "${newShop.name}" added successfully!`, 'success');
      document.getElementById('addShopModal')?.classList.remove('open');
      document.getElementById('addShopForm')?.reset();
      Complaints.populateShopSelect();
      this.handleSearch(name);
    } catch (err) {
      App.showToast('Failed to add shop', 'error');
    }
  }
};

window.Shops = Shops;
