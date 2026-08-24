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

  // Camera logic for scan.html
  const startScanBtn = document.getElementById('start-scan');
  const fileUploadInput = document.getElementById('file-upload');
  const processingOverlay = document.getElementById('processing-overlay');
  
  const videoElement = document.getElementById('camera-feed');
  const canvasElement = document.getElementById('camera-canvas');

  // Initialize camera if video element exists
  if (videoElement) {
    navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
      .then(stream => {
        videoElement.srcObject = stream;
      })
      .catch(err => {
        console.error("Camera access denied or unavailable", err);
        // Fallback gracefully (user can still use file upload)
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
          alert("Failed to capture image.");
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
        alert("There was an error analyzing the label. Please try again.");
        processingOverlay.style.display = 'none';
    }
  }
});
