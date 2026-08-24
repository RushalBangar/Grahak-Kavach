/**
 * GRAHAK KAVACH — Evidence Complaint Filing & DPDP 2023 Verification
 */

const Complaints = {
  selectedVerificationMethod: 'Aadhaar QR (Zero Storage)',
  isIdentityVerified: true,
  currentStep: 1,

  init() {
    this.bindEvents();
    this.populateShopSelect();
    this.updateRoutingPreview();
  },

  bindEvents() {
    const form = document.getElementById('complaintForm');
    const radios = document.querySelectorAll('input[name="violation_type"]');
    const tierCards = document.querySelectorAll('.verify-tier-card');
    const trackSearchBtn = document.getElementById('trackComplaintBtn');
    const trackInput = document.getElementById('trackingIdInput');

    const nextBtn = document.getElementById('wizardNextBtn');
    const backBtn = document.getElementById('wizardBackBtn');

    if (nextBtn) nextBtn.addEventListener('click', () => this.nextStep());
    if (backBtn) backBtn.addEventListener('click', () => this.prevStep());

    if (form) {
      form.addEventListener('submit', (e) => this.handleComplaintSubmit(e));
    }

    radios.forEach(r => {
      r.addEventListener('change', () => this.updateRoutingPreview());
    });

    tierCards.forEach(card => {
      card.addEventListener('click', () => {
        tierCards.forEach(c => c.classList.remove('selected'));
        card.classList.add('selected');
        this.selectedVerificationMethod = card.getAttribute('data-method');
        this.triggerVerificationModal(this.selectedVerificationMethod);
      });
    });

    if (trackSearchBtn && trackInput) {
      trackSearchBtn.addEventListener('click', () => this.searchTrackingStatus(trackInput.value.trim()));
      trackInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') this.searchTrackingStatus(trackInput.value.trim());
      });
    }
  },

  populateShopSelect() {
    const select = document.getElementById('complaintShopSelect');
    if (!select) return;

    select.innerHTML = '<option value="">-- Select Retail Shop / Store --</option>' + 
      CONFIG.INITIAL_SHOPS.map(s => `<option value="${s.id}">${s.name} (${s.address})</option>`).join('');
  },

  updateRoutingPreview() {
    const selected = document.querySelector('input[name="violation_type"]:checked')?.value || 'Both';
    const previewBadge = document.getElementById('autoRoutedBadge');
    const descText = document.getElementById('routingDescText');
    if (!previewBadge || !descText) return;

    if (selected === 'Legal Metrology') {
      previewBadge.className = 'routed-department-badge dca';
      previewBadge.innerHTML = '<i class="fas fa-balance-scale"></i> Dept. of Consumer Affairs (DCA)';
      descText.innerText = 'Packaged commodity rule violations are routed directly to the Central & State Legal Metrology Enforcement Officers.';
    } else if (selected === 'Food Safety') {
      previewBadge.className = 'routed-department-badge fssai';
      previewBadge.innerHTML = '<i class="fas fa-shield-virus"></i> FSSAI Food Safety Authority';
      descText.innerText = 'Adulteration, expiry, and hazardous ingredient complaints are forwarded to the Designated District Food Safety Officer.';
    } else {
      previewBadge.className = 'routed-department-badge both';
      previewBadge.innerHTML = '<i class="fas fa-code-branch"></i> Dual Routing: DCA + FSSAI';
      descText.innerText = 'Smart Split Engine: Generates linked dockets dispatched simultaneously to both Legal Metrology & Food Safety wings.';
    }
  },

  // DPDP 2023 Identity Verification Modal Simulation
  triggerVerificationModal(method) {
    const modal = document.getElementById('verificationSimModal');
    const title = document.getElementById('verifModalTitle');
    const body = document.getElementById('verifModalBody');
    if (!modal || !title || !body) return;

    title.innerHTML = `<i class="fas fa-shield-alt text-gradient"></i> DPDP 2023 ID Verification — ${method}`;

    if (method.includes('Aadhaar')) {
      body.innerHTML = `
        <div style="text-align: center; padding: 1rem 0;">
          <div style="width: 140px; height: 140px; margin: 0 auto 1rem; border: 2px dashed var(--accent-cyan); border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; background: rgba(6,182,212,0.05);">
            <i class="fas fa-qrcode" style="font-size: 4rem; color: var(--accent-cyan);"></i>
          </div>
          <h4 style="margin-bottom: 0.5rem;">Aadhaar Secure QR Digital Signature Scan</h4>
          <p style="font-size: 0.82rem; color: var(--text-secondary); margin-bottom: 1.25rem;">
            <strong>DPDP & Aadhaar Act Compliance:</strong> The QR code's RSA-2048 digital signature is validated offline. Zero Aadhaar numbers are captured or stored on our servers.
          </p>
          <div style="background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.3); border-radius: var(--radius-md); padding: 0.75rem; font-size: 0.85rem; color: var(--accent-emerald); display: flex; align-items: center; gap: 0.5rem; justify-content: center;">
            <i class="fas fa-check-circle"></i> Digital Signature Validated: Citizen Verified (High Trust)
          </div>
        </div>
      `;
    } else if (method.includes('DigiLocker')) {
      body.innerHTML = `
        <div style="text-align: center; padding: 1rem 0;">
          <i class="fas fa-lock" style="font-size: 3rem; color: var(--accent-blue); margin-bottom: 1rem;"></i>
          <h4>DigiLocker Consent Gateway</h4>
          <p style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 1.5rem;">
            User token exchange verified via DigiLocker Sandbox. Verified doc certificate attached as cryptographic evidence.
          </p>
          <button class="btn btn-primary btn-sm" onclick="Complaints.closeVerificationModal()">Authenticate & Confirm</button>
        </div>
      `;
    } else {
      body.innerHTML = `
        <div style="text-align: center; padding: 1rem 0;">
          <i class="fas fa-id-card" style="font-size: 3rem; color: var(--accent-amber); margin-bottom: 1rem;"></i>
          <h4>OCR ID Extraction (PAN / Voter ID)</h4>
          <p style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 1.5rem;">
            Document format validated. Masking sensitive identifiers for privacy preservation.
          </p>
          <button class="btn btn-primary btn-sm" onclick="Complaints.closeVerificationModal()">Proceed</button>
        </div>
      `;
    }

    modal.classList.add('open');
  },

  closeVerificationModal() {
    const modal = document.getElementById('verificationSimModal');
    if (modal) modal.classList.remove('open');
    App.showToast('Identity verified securely under DPDP Act 2023!', 'success');
  },


  nextStep() {
    if (this.currentStep === 1) {
      const consent = document.getElementById('consentCheckbox');
      if (!consent || !consent.checked) {
        App.showToast('Please consent to identity verification to proceed.', 'warning');
        return;
      }
      this.isIdentityVerified = true;
    }

    if (this.currentStep === 2) {
      const shopId = document.getElementById('complaintShopSelect').value;
      const prodDetails = document.getElementById('complaintProductDetails').value;
      if (!shopId) {
        App.showToast('Please select a retail shop.', 'warning');
        return;
      }
      if (!prodDetails.trim()) {
        App.showToast('Please describe the product and issue.', 'warning');
        return;
      }
      // Populate review section
      document.getElementById('reviewIdentity').innerText = this.selectedVerificationMethod;
      document.getElementById('reviewIssue').innerText = prodDetails;
      document.getElementById('reviewVendor').innerText = document.getElementById('complaintShopSelect').options[document.getElementById('complaintShopSelect').selectedIndex].text;
      document.getElementById('reviewRouting').innerText = document.querySelector('input[name="violation_type"]:checked')?.value || 'Both';
    }

    if (this.currentStep === 3) {
      this.submitComplaint();
      return;
    }

    this.currentStep++;
    this.updateWizardUI();
  },

  prevStep() {
    if (this.currentStep > 1) {
      this.currentStep--;
      this.updateWizardUI();
    }
  },

  updateWizardUI() {
    // Update steps
    for (let i = 1; i <= 3; i++) {
      const stepEl = document.getElementById('step' + i);
      const trackerEl = document.getElementById('trackerStep' + i);
      
      if (stepEl) {
        if (i === this.currentStep) {
          stepEl.classList.add('active');
          stepEl.style.opacity = '1';
          stepEl.style.pointerEvents = 'auto';
        } else {
          stepEl.classList.remove('active');
          stepEl.style.opacity = '0.5';
          stepEl.style.pointerEvents = 'none';
        }
      }

      if (trackerEl) {
        if (i <= this.currentStep) {
          trackerEl.style.opacity = '1';
        } else {
          trackerEl.style.opacity = '0.5';
        }
      }
    }

    // Update buttons
    const nextBtn = document.getElementById('wizardNextBtn');
    const backBtn = document.getElementById('wizardBackBtn');
    
    if (backBtn) {
      backBtn.style.visibility = this.currentStep === 1 ? 'hidden' : 'visible';
    }
    
    if (nextBtn) {
      if (this.currentStep === 3) {
        nextBtn.innerHTML = 'Submit Grievance <span class="material-symbols-outlined text-sm">gavel</span>';
        nextBtn.classList.remove('bg-primary');
        nextBtn.classList.add('bg-error');
      } else {
        nextBtn.innerHTML = 'Next Step <span class="material-symbols-outlined text-sm">arrow_forward</span>';
        nextBtn.classList.add('bg-primary');
        nextBtn.classList.remove('bg-error');
      }
    }
  },

  submitComplaint() {
    // Call the original submit logic directly
    const mockEvent = { preventDefault: () => {} };
    this.handleComplaintSubmit(mockEvent);
  },

  async handleComplaintSubmit(e) {
    e.preventDefault();
    const shopId = document.getElementById('complaintShopSelect').value;
    const prodDetails = document.getElementById('complaintProductDetails').value;
    const violationType = document.querySelector('input[name="violation_type"]:checked')?.value || 'Both';
    const evidenceInput = document.getElementById('complaintEvidenceInput');

    if (!shopId) {
      App.showToast('Please select a retail shop.', 'warning');
      return;
    }

    if (!prodDetails.trim()) {
      App.showToast('Please specify the product details and violation description.', 'warning');
      return;
    }

    const payload = {
      shop_id: parseInt(shopId),
      product_details: prodDetails,
      violation_type: violationType,
      verification_method: this.selectedVerificationMethod,
      evidence_url: evidenceInput?.value || 'evidence_upload_label.jpg'
    };

    App.showToast('Submitting verified complaint...', 'info');

    try {
      const result = await API.fileComplaint(payload);
      this.showComplaintReceipt(result);
      document.getElementById('complaintForm').reset();
      this.populateShopSelect();
    } catch (err) {
      App.showToast('Error filing complaint', 'error');
    }
  },

  showComplaintReceipt(complaint) {
    const modal = document.getElementById('receiptModal');
    const trkIdEl = document.getElementById('receiptTrackingId');
    const deptEl = document.getElementById('receiptDepartment');
    const statusEl = document.getElementById('receiptStatus');
    const dateEl = document.getElementById('receiptDate');

    if (trkIdEl) trkIdEl.innerText = complaint.tracking_id;
    if (deptEl) deptEl.innerText = complaint.routed_to === 'Both' ? 'DCA & FSSAI (Dual Split)' : complaint.routed_to;
    if (statusEl) statusEl.innerText = complaint.status || 'Verified & Queued for Enforcement';
    if (dateEl) dateEl.innerText = new Date(complaint.date_filed).toLocaleString();

    if (modal) modal.classList.add('open');
  },

  // Public Complaint Status Tracker
  async searchTrackingStatus(trackingId) {
    if (!trackingId) {
      App.showToast('Please enter a Tracking ID (e.g. GK-8F2B1A)', 'warning');
      return;
    }

    try {
      const complaint = await API.getComplaint(trackingId);
      this.renderTrackingTimeline(complaint);
      App.showToast(`Found tracking record for ${trackingId.toUpperCase()}`, 'success');
    } catch (err) {
      App.showToast('Tracking ID not found.', 'error');
    }
  },

  renderTrackingTimeline(complaint) {
    const timelineContainer = document.getElementById('trackingTimelineResults');
    if (!timelineContainer) return;

    timelineContainer.style.display = 'block';
    timelineContainer.innerHTML = `
      <div class="glass-card" style="margin-top: 1.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.5rem; flex-wrap: wrap; gap: 1rem;">
          <div>
            <div style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--accent-cyan); font-weight: 700;">TRACKING ID</div>
            <h3 style="font-size: 1.5rem; font-family: var(--font-mono);">${complaint.tracking_id}</h3>
          </div>
          <span class="routed-department-badge ${complaint.routed_to?.toLowerCase() || 'both'}">
            <i class="fas fa-paper-plane"></i> Routed: ${complaint.routed_to}
          </span>
        </div>

        <div style="font-size: 0.88rem; margin-bottom: 1.5rem; background: rgba(0,0,0,0.25); padding: 0.85rem; border-radius: var(--radius-md); border: 1px solid var(--border-subtle);">
          <strong>Violation Dossier:</strong> ${complaint.product_details}
          <div style="margin-top: 0.4rem; color: var(--accent-emerald); font-size: 0.78rem;">
            <i class="fas fa-user-check"></i> Identity: ${complaint.verification_method} (DPDP Compliant)
          </div>
        </div>

        <div class="timeline">
          <div class="timeline-step completed">
            <div class="step-marker"><i class="fas fa-check"></i></div>
            <div class="step-content">
              <h4>Complaint Logged & ID Verified</h4>
              <p>Digital signature confirmed under DPDP Act 2023. Authenticated proof dossier created.</p>
              <span class="step-date">${new Date(complaint.date_filed).toLocaleDateString()}</span>
            </div>
          </div>
          <div class="timeline-step completed">
            <div class="step-marker"><i class="fas fa-check"></i></div>
            <div class="step-content">
              <h4>Auto-Routed to Regulatory Wing</h4>
              <p>Docket dispatched to ${complaint.routed_to} jurisdiction enforcement queue.</p>
              <span class="step-date">Automated AI Routing Engine</span>
            </div>
          </div>
          <div class="timeline-step active">
            <div class="step-marker"><i class="fas fa-sync-alt fa-spin"></i></div>
            <div class="step-content">
              <h4>Assigned to Zonal Enforcement Officer</h4>
              <p>Prioritized in Officer inspection dashboard for physical or surprise audit.</p>
              <span class="step-date">Current Status: ${complaint.status}</span>
            </div>
          </div>
          <div class="timeline-step">
            <div class="step-marker"><i class="fas fa-clock"></i></div>
            <div class="step-content">
              <h4>Action & Compounding Resolution</h4>
              <p>Fine settlement, notice issuance, or court compounding update.</p>
              <span class="step-date">Pending inspection closure</span>
            </div>
          </div>
        </div>
      </div>
    `;
  }
};

window.Complaints = Complaints;
