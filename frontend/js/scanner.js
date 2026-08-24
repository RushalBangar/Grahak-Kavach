/**
 * GRAHAK KAVACH — AI Label Scanner & Dual Engine Visualizer
 */

const Scanner = {
  currentScannedResult: null,
  activeStream: null,

  init() {
    this.bindEvents();
    this.renderPresets();
  },

  bindEvents() {
    const dropzone = document.getElementById('scanDropzone');
    const fileInput = document.getElementById('labelFileInput');
    const uploadBtn = document.getElementById('uploadFileBtn');
    const cameraBtn = document.getElementById('openCameraBtn');
    const captureBtn = document.getElementById('capturePhotoBtn');
    const closeCamBtn = document.getElementById('closeCameraBtn');
    const fileComplaintFromScanBtn = document.getElementById('fileComplaintFromScanBtn');

    if (uploadBtn && fileInput) {
      uploadBtn.addEventListener('click', () => fileInput.click());
      fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
    }

    if (dropzone) {
      dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.classList.add('dragover');
      });
      dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));
      dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.classList.remove('dragover');
        if (e.dataTransfer.files.length) {
          this.processImageFile(e.dataTransfer.files[0]);
        }
      });
    }

    if (cameraBtn) {
      cameraBtn.addEventListener('click', () => this.startCamera());
    }

    if (captureBtn) {
      captureBtn.addEventListener('click', () => this.captureCameraFrame());
    }

    if (closeCamBtn) {
      closeCamBtn.addEventListener('click', () => this.stopCamera());
    }

    if (fileComplaintFromScanBtn) {
      fileComplaintFromScanBtn.addEventListener('click', () => this.prefillComplaintWizard());
    }
  },

  // Render Preset Cards for instant judge testing
  renderPresets() {
    const container = document.getElementById('presetList');
    if (!container) return;

    container.innerHTML = CONFIG.PRESETS.map(preset => `
      <button class="preset-btn" onclick="Scanner.loadPreset('${preset.id}')">
        <span class="preset-tag ${preset.tagType}">${preset.category}</span>
        <strong>${preset.title}</strong>
      </button>
    `).join('');
  },

  // Load a preset for instant zero-friction demo
  loadPreset(presetId) {
    const preset = CONFIG.PRESETS.find(p => p.id === presetId);
    if (!preset) return;

    // Show preview image
    const previewBox = document.getElementById('previewContainer');
    const previewImg = document.getElementById('previewImage');
    if (previewBox && previewImg) {
      previewImg.src = preset.image;
      previewBox.classList.add('active');
    }

    this.startScanAnimation();

    setTimeout(() => {
      this.stopScanAnimation();
      this.currentScannedResult = preset;
      this.renderResults(preset);
      App.showToast(`Analyzed ${preset.title}`, 'success');
    }, 900);
  },

  handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
      this.processImageFile(file);
    }
  },

  processImageFile(file) {
    const previewBox = document.getElementById('previewContainer');
    const previewImg = document.getElementById('previewImage');
    const statusText = document.querySelector('#view_scanner .font-label-caps.text-ai-accent');

    const reader = new FileReader();
    reader.onload = (e) => {
      if (previewImg && previewBox) {
        previewImg.src = e.target.result;
        previewBox.classList.add('active');
      }
    };
    reader.readAsDataURL(file);

    this.startScanAnimation();
    if (statusText) statusText.innerText = 'Reading label...';

    setTimeout(() => {
      if (statusText) statusText.innerText = 'Checking compliance...';
      
      setTimeout(() => {
        if (statusText) statusText.innerText = 'Analyzing ingredients...';
        
        API.analyzeLabel(file).then(result => {
          this.stopScanAnimation();
          if (statusText) statusText.innerText = 'Visual OCR Active';
          this.currentScannedResult = result;
          this.renderResults(result);
          App.showToast('Product Label Analysis Complete!', 'success');
        }).catch(err => {
          this.stopScanAnimation();
          if (statusText) statusText.innerText = 'Visual OCR Active';
          App.showToast('Failed to analyze label', 'error');
        });
      }, 1000);
    }, 1000);
  },

  // Camera Live Capture
  async startCamera() {
    const modal = document.getElementById('cameraModal');
    const video = document.getElementById('cameraVideo');
    if (!modal || !video) return;

    try {
      this.activeStream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment' },
        audio: false
      });
      video.srcObject = this.activeStream;
      video.play();
      modal.classList.add('open');
    } catch (err) {
      App.showToast('Unable to access camera. Please check permissions.', 'warning');
    }
  },

  captureCameraFrame() {
    const video = document.getElementById('cameraVideo');
    const canvas = document.createElement('canvas');
    if (!video) return;

    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(blob => {
      this.stopCamera();
      this.processImageFile(blob);
    }, 'image/jpeg');
  },

  stopCamera() {
    const modal = document.getElementById('cameraModal');
    if (modal) modal.classList.remove('open');
    if (this.activeStream) {
      this.activeStream.getTracks().forEach(track => track.stop());
      this.activeStream = null;
    }
  },

  startScanAnimation() {
    const scanLine = document.getElementById('scanLine');
    if (scanLine) scanLine.classList.add('scanning');
  },

  stopScanAnimation() {
    const scanLine = document.getElementById('scanLine');
    if (scanLine) scanLine.classList.remove('scanning');
  },

  // Render Dual Results View
  renderResults(data) {
    const placeholder = document.getElementById('resultsPlaceholder');
    const content = document.getElementById('resultsContent');
    const container = document.getElementById('resultsContainer');
    if (!content) return;

    if (placeholder) placeholder.style.display = 'none';
    if (container) {
      container.style.display = 'block';
      container.classList.add('active');
    }
    content.classList.add('active');

    // 1. Legal Metrology Module
    const lm = data.legal_metrology || {};
    const isLmCompliant = lm.is_compliant;
    const lmBadge = document.getElementById('lmComplianceBadge');
    const lmDetails = document.getElementById('lmDetailsText');
    const lmChecklist = document.getElementById('lmChecklist');

    if (lmBadge) {
      lmBadge.className = `compliance-badge ${isLmCompliant ? 'pass' : 'fail'}`;
      lmBadge.innerHTML = isLmCompliant 
        ? '<i class="fas fa-check-circle"></i> Fully Compliant (2011 Rules)'
        : '<i class="fas fa-exclamation-triangle"></i> Violations Detected';
    }

    if (lmDetails) {
      lmDetails.innerText = lm.details || 'Legal Metrology mandatory declarations evaluated.';
    }

    if (lmChecklist) {
      const checks = lm.checklist || {
        has_mrp: isLmCompliant,
        has_qty: isLmCompliant,
        has_mfg_date: isLmCompliant,
        has_expiry_date: true,
        has_manufacturer: true
      };

      lmChecklist.innerHTML = `
        <div class="check-item ${checks.has_mrp ? 'valid' : 'missing'}">
          <i class="fas ${checks.has_mrp ? 'fa-check' : 'fa-times'}"></i> MRP & Max Sale Price
        </div>
        <div class="check-item ${checks.has_qty ? 'valid' : 'missing'}">
          <i class="fas ${checks.has_qty ? 'fa-check' : 'fa-times'}"></i> Net Quantity / Volume
        </div>
        <div class="check-item ${checks.has_mfg_date ? 'valid' : 'missing'}">
          <i class="fas ${checks.has_mfg_date ? 'fa-check' : 'fa-times'}"></i> Mfg / Packaging Date
        </div>
        <div class="check-item ${checks.has_expiry_date ? 'valid' : 'missing'}">
          <i class="fas ${checks.has_expiry_date ? 'fa-check' : 'fa-times'}"></i> Expiry / Best Before
        </div>
        <div class="check-item ${checks.has_manufacturer ? 'valid' : 'missing'}">
          <i class="fas ${checks.has_manufacturer ? 'fa-check' : 'fa-times'}"></i> Manufacturer & Care Address
        </div>
      `;
    }

    // 2. Food Safety & Health Score Module
    const fs = data.food_safety || {};
    const healthScore = (fs.health_score || 'B').toUpperCase();
    const harmfulList = fs.harmful_ingredients || [];

    // Highlight Nutri-Score scale
    ['A', 'B', 'C', 'D', 'E'].forEach(letter => {
      const box = document.getElementById(`scoreBox_${letter}`);
      if (box) {
        if (letter === healthScore) box.classList.add('active-score');
        else box.classList.remove('active-score');
      }
    });

    const harmfulContainer = document.getElementById('harmfulIngredientsList');
    if (harmfulContainer) {
      if (harmfulList.length === 0) {
        harmfulContainer.innerHTML = `<span style="font-size: 0.85rem; color: var(--accent-emerald);"><i class="fas fa-shield-alt"></i> No restricted, banned, or hazardous food additives found.</span>`;
      } else {
        harmfulContainer.innerHTML = harmfulList.map(item => `
          <span class="harmful-tag">
            <i class="fas fa-biohazard"></i> ${item}
          </span>
        `).join('');
      }
    }

    const fsDetails = document.getElementById('fsDetailsText');
    if (fsDetails) {
      fsDetails.innerText = fs.details || `Health Grade: ${healthScore}. Screened under FSSAI 2020 Display Regulations.`;
    }

    // 3. Raw OCR Extracted Text
    const ocrBox = document.getElementById('extractedOcrText');
    if (ocrBox) {
      ocrBox.innerText = data.extracted_text || 'No text extracted.';
    }
  },

  // Bridge: Pre-fill Complaint wizard with scanned results
  prefillComplaintWizard() {
    if (!this.currentScannedResult) return;

    App.switchView('complaints');

    const prodDetails = document.getElementById('complaintProductDetails');
    const violationBoth = document.getElementById('violation_both');
    const violationLm = document.getElementById('violation_lm');
    const violationFs = document.getElementById('violation_fs');

    if (prodDetails) {
      prodDetails.value = this.currentScannedResult.title || 'Scanned Packaged Commodity with detected violations.';
    }

    const isLmBad = !this.currentScannedResult.legal_metrology?.is_compliant;
    const isFsBad = (this.currentScannedResult.food_safety?.harmful_ingredients?.length || 0) > 0 || ['D', 'E'].includes(this.currentScannedResult.food_safety?.health_score);

    if (isLmBad && isFsBad && violationBoth) {
      violationBoth.checked = true;
    } else if (isLmBad && violationLm) {
      violationLm.checked = true;
    } else if (violationFs) {
      violationFs.checked = true;
    }

    Complaints.updateRoutingPreview();
    App.showToast('Scan details transferred to Complaint form!', 'success');
  }
};

window.Scanner = Scanner;
