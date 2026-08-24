// main.js

document.addEventListener('DOMContentLoaded', () => {
  // Simple navigation handling for active states in bottom nav
  const navItems = document.querySelectorAll('.nav-item');
  const currentPath = window.location.pathname;

  navItems.forEach(item => {
    if (item.getAttribute('href') && currentPath.includes(item.getAttribute('href'))) {
      item.classList.add('active');
    }
  });

  // Camera mock logic for scan.html
  const startScanBtn = document.getElementById('start-scan');
  const fileUploadInput = document.getElementById('file-upload');
  const processingOverlay = document.getElementById('processing-overlay');

  if (startScanBtn && processingOverlay) {
    startScanBtn.addEventListener('click', () => {
      startProcessing();
    });
  }

  if (fileUploadInput && processingOverlay) {
    fileUploadInput.addEventListener('change', (e) => {
      if (e.target.files.length > 0) {
        startProcessing();
      }
    });
  }

  function startProcessing() {
    processingOverlay.classList.remove('hidden');
    processingOverlay.style.display = 'flex';
    
    // Simulate OCR and API call delay
    setTimeout(() => {
      window.location.href = 'results.html';
    }, 2500);
  }
});
