/**
 * GRAHAK KAVACH — Main Application Controller & UI Orchestrator
 */

const App = {
  currentView: 'landing',

  init() {
    this.setupTheme();
    this.setupNavigation();
    this.setupModals();
    this.checkBackendConnectivity();

    // Initialize all sub-modules
    Scanner.init();
    Complaints.init();
    Shops.init();
    Officer.init();

    console.log('🛡️ Grahak Kavach Platform Initialized (SIH 2026)');
  },

  // Switch SPA Views
  switchView(viewName) {
    this.currentView = viewName;

    const mainNav = document.getElementById('main-nav');
    const mobileNav = document.querySelector('nav.fixed.bottom-0');
    
    if (viewName === 'landing' || viewName === 'officer_login') {
      if (mainNav) mainNav.style.display = 'none';
      if (mobileNav) mobileNav.style.display = 'none';
    } else {
      if (mainNav) mainNav.style.display = '';
      if (mobileNav) mobileNav.style.display = '';
    }

    // Update Nav Tab Buttons
    document.querySelectorAll('.nav-tab-btn').forEach(btn => {
      if (btn.getAttribute('data-view') === viewName) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });

    // Update View Containers
    document.querySelectorAll('.app-view').forEach(view => {
      if (view.id === `view_${viewName}`) {
        view.classList.add('active-view');
      } else {
        view.classList.remove('active-view');
      }
    });

    window.scrollTo({ top: 0, behavior: 'smooth' });
  },

  setupNavigation() {
    document.querySelectorAll('.nav-tab-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const view = btn.getAttribute('data-view');
        this.switchView(view);
      });
    });
  },

  setupTheme() {
    const themeBtn = document.getElementById('themeToggleBtn');
    const savedTheme = localStorage.getItem('gk_theme') || 'dark';

    document.documentElement.setAttribute('data-theme', savedTheme);
    this.updateThemeIcon(savedTheme);

    if (themeBtn) {
      themeBtn.addEventListener('click', () => {
        const current = document.documentElement.getAttribute('data-theme');
        const next = current === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', next);
        localStorage.setItem('gk_theme', next);
        this.updateThemeIcon(next);
      });
    }
  },

  updateThemeIcon(theme) {
    const icon = document.querySelector('#themeToggleBtn i');
    if (icon) {
      icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }
  },

  setupModals() {
    // Close modal on backdrop click or close button
    document.querySelectorAll('.modal-backdrop').forEach(modal => {
      modal.addEventListener('click', (e) => {
        if (e.target === modal) {
          modal.classList.remove('open');
          if (modal.id === 'cameraModal') Scanner.stopCamera();
        }
      });
    });

    document.querySelectorAll('.modal-close').forEach(btn => {
      btn.addEventListener('click', () => {
        const modal = btn.closest('.modal-backdrop');
        if (modal) {
          modal.classList.remove('open');
          if (modal.id === 'cameraModal') Scanner.stopCamera();
        }
      });
    });
  },

  async checkBackendConnectivity() {
    const pill = document.getElementById('backendStatusPill');
    const isOnline = await API.checkHealth();

    if (pill) {
      if (isOnline) {
        pill.className = 'backend-pill';
        pill.innerHTML = '<span class="status-dot"></span> Backend Live (Render Cloud)';
      } else {
        pill.className = 'backend-pill offline';
        pill.innerHTML = '<span class="status-dot"></span> Offline Demo Mode';
      }
    }
  },

  // Global Toast Notifications
  showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;

    let icon = 'info-circle';
    if (type === 'success') icon = 'check-circle';
    if (type === 'error') icon = 'exclamation-circle';
    if (type === 'warning') icon = 'exclamation-triangle';

    toast.innerHTML = `
      <div style="display: flex; align-items: center; gap: 0.6rem;">
        <i class="fas fa-${icon}"></i>
        <span>${message}</span>
      </div>
      <button style="background:none;border:none;color:inherit;cursor:pointer;margin-left:0.75rem;" onclick="this.parentElement.remove()">
        <i class="fas fa-times"></i>
      </button>
    `;

    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      toast.style.transition = 'all 0.3s ease-out';
      setTimeout(() => toast.remove(), 300);
    }, 4000);
  }
};

document.addEventListener('DOMContentLoaded', () => {
  App.init();
});

window.App = App;
