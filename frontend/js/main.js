// main.js

// Global Toast Utility
window.showToast = function(message, type = 'default') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  
  let icon = '';
  if (type === 'error') icon = '<svg style="color:var(--danger)" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>';
  else if (type === 'success') icon = '<svg style="color:var(--success)" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>';
  else if (type === 'warning') icon = '<svg style="color:var(--warning)" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>';

  toast.innerHTML = `${icon} <span>${message}</span>`;
  container.appendChild(toast);

  // Trigger animation
  requestAnimationFrame(() => {
    toast.classList.add('show');
  });

  // Remove after 3s
  setTimeout(() => {
    toast.classList.remove('show');
    toast.addEventListener('transitionend', () => toast.remove());
  }, 3000);
};

document.addEventListener('DOMContentLoaded', () => {
  // Simple navigation handling for active states in bottom nav
  const navItems = document.querySelectorAll('.nav-item');
  const currentPath = window.location.pathname;

  navItems.forEach(item => {
    if (item.getAttribute('href') && currentPath.includes(item.getAttribute('href'))) {
      item.classList.add('active');
    }
  });

  // Camera logic for scan.html
  const startScanBtn = document.getElementById('start-scan');
  const fileUploadInput = document.getElementById('file-upload');
  const processingOverlay = document.getElementById('processing-overlay');
  
  const videoElement = document.getElementById('camera-feed');
  const canvasElement = document.getElementById('camera-canvas');
  const flashBtn = document.getElementById('toggle-flash');

  let currentStream = null;
  let flashEnabled = false;

  // Initialize camera if video element exists
  if (videoElement) {
    navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
      .then(stream => {
        currentStream = stream;
        videoElement.srcObject = stream;
        
        // Setup flashlight button if supported
        const track = stream.getVideoTracks()[0];
        const imageCapture = new ImageCapture(track);
        imageCapture.getPhotoCapabilities().then(caps => {
            if (!caps.fillLightMode) {
                if (flashBtn) flashBtn.style.display = 'none'; // Not supported
            }
        }).catch(() => {
            if (flashBtn) flashBtn.style.display = 'none'; // Not supported or error
        });

        if (flashBtn) {
            flashBtn.addEventListener('click', async () => {
                flashEnabled = !flashEnabled;
                try {
                    await track.applyConstraints({
                        advanced: [{ torch: flashEnabled }]
                    });
                    flashBtn.style.background = flashEnabled ? 'var(--primary-color)' : 'rgba(0,0,0,0.5)';
                } catch (e) {
                    console.log("Torch not supported", e);
                }
            });
        }
      })
      .catch(err => {
        console.error("Camera access denied or unavailable", err);
      });
  }

  if (startScanBtn && processingOverlay && videoElement && canvasElement) {
    startScanBtn.addEventListener('click', () => {
      // Draw current video frame to canvas
      const context = canvasElement.getContext('2d');
      canvasElement.width = videoElement.videoWidth;
      canvasElement.height = videoElement.videoHeight;
      context.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);
      
      // Convert canvas to blob/file
      canvasElement.toBlob(blob => {
        if (blob) {
          const file = new File([blob], "capture.jpg", { type: "image/jpeg" });
          startProcessing(file);
        } else {
          showToast("Failed to capture image.", "error");
        }
      }, 'image/jpeg', 0.9);
    });
  }

  if (fileUploadInput && processingOverlay) {
    fileUploadInput.addEventListener('change', async (e) => {
      if (e.target.files.length > 0) {
        await startProcessing(e.target.files[0]);
      }
    });
  }

  async function startProcessing(file) {
    processingOverlay.classList.remove('hidden');
    processingOverlay.style.display = 'flex';
    
    try {
        // Only works if api.js is loaded
        if (typeof API !== 'undefined' && file) {
            const result = await API.scan(file);
            sessionStorage.setItem('scanResult', JSON.stringify(result));
            window.location.href = 'results.html';
        } else {
            // Mock fallback if no file or API
            setTimeout(() => {
                window.location.href = 'results.html';
            }, 2500);
        }
    } catch (error) {
        console.error("Scan error:", error);
        showToast("There was an error analyzing the label. Please try again.", "error");
        processingOverlay.style.display = 'none';
    }
  }
});
