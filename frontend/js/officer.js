/**
 * GRAHAK KAVACH — Officer Enforcement Suite & Department Portals
 */

const Officer = {
  init() {
    this.bindEvents();
    this.checkSession();
  },

  bindEvents() {
    const loginForm = document.getElementById('officerLoginForm');
    const logoutBtn = document.getElementById('officerLogoutBtn');
    const openLogInspBtn = document.getElementById('openLogInspectionBtn');
    const inspectionForm = document.getElementById('logInspectionForm');

    if (loginForm) {
      loginForm.addEventListener('submit', (e) => this.handleLogin(e));
    }

    if (logoutBtn) {
      logoutBtn.addEventListener('click', () => this.handleLogout());
    }

    if (openLogInspBtn) {
      openLogInspBtn.addEventListener('click', () => this.openInspectionModal());
    }

    if (inspectionForm) {
      inspectionForm.addEventListener('submit', (e) => this.handleInspectionSubmit(e));
    }
  },

  checkSession() {
    const token = localStorage.getItem('gk_officer_token');
    const authView = document.getElementById('officerAuthView');
    const dashView = document.getElementById('officerDashboardView');

    if (token) {
      if (authView) authView.style.display = 'none';
      if (dashView) dashView.style.display = 'block';
      this.loadDashboardData();
    } else {
      if (authView) authView.style.display = 'block';
      if (dashView) dashView.style.display = 'none';
    }
  },

  async handleLogin(e) {
    e.preventDefault();
    const user = document.getElementById('officerUsername').value.trim();
    const pass = document.getElementById('officerPassword').value.trim();

    if (!user || !pass) {
      App.showToast('Please enter both username and password.', 'warning');
      return;
    }

    try {
      await API.officerLogin(user, pass);
      App.showToast('Officer Login Successful. Welcome, Inspector!', 'success');
      this.checkSession();
    } catch (err) {
      App.showToast(err.message || 'Login failed', 'error');
    }
  },

  handleLogout() {
    localStorage.removeItem('gk_officer_token');
    localStorage.removeItem('gk_officer_user');
    App.showToast('Logged out from Officer Portal.', 'info');
    this.checkSession();
  },

  async loadDashboardData() {
    const tableBody = document.getElementById('officerInspectionsTableBody');
    const shopSelect = document.getElementById('inspShopSelect');

    // Populate shop select in modal
    if (shopSelect) {
      shopSelect.innerHTML = '<option value="">-- Choose Shop Under Inspection --</option>' +
        CONFIG.INITIAL_SHOPS.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
    }

    try {
      const inspections = await API.getOfficerInspections();
      
      // Update metric numbers
      const totalCount = inspections.length;
      const violationsCount = inspections.filter(i => !i.is_compliant).length;
      const passCount = inspections.filter(i => i.is_compliant).length;

      const metricTotal = document.getElementById('metricTotalInsp');
      const metricViolations = document.getElementById('metricViolations');
      const metricPass = document.getElementById('metricPass');

      if (metricTotal) metricTotal.innerText = totalCount;
      if (metricViolations) metricViolations.innerText = violationsCount;
      if (metricPass) metricPass.innerText = passCount;

      if (tableBody) {
        tableBody.innerHTML = inspections.map(i => {
          const shop = CONFIG.INITIAL_SHOPS.find(s => s.id === i.shop_id) || { name: `Shop #${i.shop_id}` };
          return `
            <tr>
              <td><strong>${shop.name}</strong></td>
              <td>${i.product_scanned}</td>
              <td>
                <span class="status-tag ${i.is_compliant ? 'pass' : 'violation'}">
                  <i class="fas ${i.is_compliant ? 'fa-check' : 'fa-times'}"></i> ${i.is_compliant ? 'Pass' : 'Violation'}
                </span>
              </td>
              <td style="max-width: 250px;">${i.violation_details || 'Standard verification passed.'}</td>
              <td style="font-family: var(--font-mono); font-size: 0.78rem;">${new Date(i.date_logged).toLocaleDateString()}</td>
            </tr>
          `;
        }).join('');
      }
    } catch (err) {
      console.error('Dashboard load failed:', err);
    }
  },

  openInspectionModal() {
    const modal = document.getElementById('logInspectionModal');
    if (modal) modal.classList.add('open');
  },

  async handleInspectionSubmit(e) {
    e.preventDefault();
    const shopId = document.getElementById('inspShopSelect').value;
    const prodName = document.getElementById('inspProductName').value.trim();
    const isCompliant = document.getElementById('inspIsCompliant').value === 'true';
    const details = document.getElementById('inspViolationDetails').value.trim();

    if (!shopId || !prodName) {
      App.showToast('Please select shop and product name.', 'warning');
      return;
    }

    const payload = {
      shop_id: parseInt(shopId),
      product_scanned: prodName,
      is_compliant: isCompliant,
      violation_details: details || (isCompliant ? 'Compliant with packaged rules' : 'Violation identified and compounded')
    };

    try {
      await API.logInspection(payload);
      App.showToast('Inspection entry officially logged to Legal Metrology database!', 'success');
      document.getElementById('logInspectionModal')?.classList.remove('open');
      document.getElementById('logInspectionForm')?.reset();
      this.loadDashboardData();
    } catch (err) {
      App.showToast('Failed to save inspection', 'error');
    }
  }
};

window.Officer = Officer;
