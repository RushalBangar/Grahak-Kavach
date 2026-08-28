const I18N = {
  currentLang: localStorage.getItem('grahak_lang') || 'en',

  init() {
    this.applyTranslations();
    this.setupSwitcher();
  },

  setLanguage(lang) {
    if (translations[lang]) {
      this.currentLang = lang;
      localStorage.setItem('grahak_lang', lang);
      this.applyTranslations();
      // Update switcher if it exists
      const switchers = document.querySelectorAll('.lang-switcher');
      switchers.forEach(switcher => {
        switcher.value = lang;
      });
    }
  },

  applyTranslations() {
    const elements = document.querySelectorAll('[data-i18n]');
    const dict = translations[this.currentLang] || translations['en'];

    elements.forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (dict[key]) {
        if (el.tagName.toLowerCase() === 'input' || el.tagName.toLowerCase() === 'textarea') {
          el.placeholder = dict[key];
        } else {
          el.innerHTML = dict[key];
        }
      }
    });
  },

  setupSwitcher() {
    const switchers = document.querySelectorAll('.lang-switcher');
    switchers.forEach(switcher => {
      switcher.value = this.currentLang;
      switcher.addEventListener('change', (e) => {
        this.setLanguage(e.target.value);
      });
    });
  }
};

document.addEventListener('DOMContentLoaded', () => {
  if (typeof translations !== 'undefined') {
    I18N.init();
  }
});
