/**
 * GRAHAK KAVACH — API Client Service
 * Communicates with FastAPI backend with graceful fallback simulation.
 */

const API = {
  // Check backend server health
  async checkHealth() {
    try {
      const res = await fetch(`${CONFIG.API_BASE_URL}/docs`, { mode: 'no-cors' });
      CONFIG.DEMO_MODE_ACTIVE = false;
      return true;
    } catch (err) {
      console.warn('Health check failed, activating offline demo mode:', err);
      CONFIG.DEMO_MODE_ACTIVE = true;
      return false;
    }
  },

  // 1. Analyze Label via Backend OCR + AI engine
  async analyzeLabel(fileOrBlob) {
    try {
      const formData = new FormData();
      formData.append('file', fileOrBlob);

      const response = await fetch(`${CONFIG.API_BASE_URL}/api/scan/analyze`, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) throw new Error('API Scan failed');
      return await response.json();
    } catch (error) {
      console.warn('Backend unavailable, using AI offline engine simulation:', error);
      // Generate intelligent offline analysis
      return API.simulateScanResult();
    }
  },

  // Fallback offline scan simulator
  simulateScanResult() {
    return {
      extracted_text: `SAMPLE EXTRACTED PRODUCT LABEL
Ingredients: Refined Wheat, Sugar, Hydrogenated Palm Oil, Tartrazine (E102), Salt.
Net Qty: 150g | MRP: Rs. 45.00 | Mfg: 01/2026`,
      legal_metrology: {
        is_compliant: true,
        details: 'Found MRP: true, Net Qty: true, Mfg Date: true (Legal Metrology Rules 2011 Compliant)'
      },
      food_safety: {
        health_score: 'C',
        harmful_ingredients: ['tartrazine', 'hydrogenated palm oil']
      }
    };
  },

  // 2. Search Shops
  async searchShops(query) {
    try {
      const response = await fetch(`${CONFIG.API_BASE_URL}/api/shops/search?query=${encodeURIComponent(query)}`);
      if (!response.ok) throw new Error('Shop search failed');
      return await response.json();
    } catch (error) {
      // Local fallback filter
      return CONFIG.INITIAL_SHOPS.filter(s => 
        s.name.toLowerCase().includes(query.toLowerCase()) || 
        s.address.toLowerCase().includes(query.toLowerCase())
      );
    }
  },

  // 3. Create Shop
  async createShop(shopData) {
    try {
      const response = await fetch(`${CONFIG.API_BASE_URL}/api/shops/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(shopData)
      });
      if (!response.ok) throw new Error('Create shop failed');
      return await response.json();
    } catch (error) {
      const newShop = {
        id: Math.floor(Math.random() * 1000) + 10,
        name: shopData.name,
        address: shopData.address
      };
      CONFIG.INITIAL_SHOPS.push(newShop);
      return newShop;
    }
  },

  // 4. Get Shop Compliance History
  async getShopHistory(shopId) {
    try {
      const response = await fetch(`${CONFIG.API_BASE_URL}/api/shops/${shopId}/history`);
      if (!response.ok) throw new Error('Failed to get shop history');
      return await response.json();
    } catch (error) {
      const shop = CONFIG.INITIAL_SHOPS.find(s => s.id === parseInt(shopId)) || CONFIG.INITIAL_SHOPS[0];
      return {
        shop: {
          id: shop.id,
          name: shop.name,
          address: shop.address
        },
        inspections: [
          {
            date: new Date(Date.now() - 86400000 * 12).toISOString(),
            is_compliant: true,
            details: 'Routine Legal Metrology check. All MRP and weight declarations standard.'
          },
          {
            date: new Date(Date.now() - 86400000 * 45).toISOString(),
            is_compliant: false,
            details: 'Dual overcharging violation detected on packaged dairy products (Fine Compounded: Rs. 5000).'
          }
        ],
        resolved_complaints: [
          {
            tracking_id: 'GK-8F2B1A',
            date: new Date(Date.now() - 86400000 * 18).toISOString(),
            violation_type: 'Legal Metrology'
          }
        ]
      };
    }
  },

  // 5. File Complaint
  async fileComplaint(complaintData) {
    try {
      const response = await fetch(`${CONFIG.API_BASE_URL}/api/complaints/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(complaintData)
      });
      if (!response.ok) throw new Error('Failed to file complaint');
      return await response.json();
    } catch (error) {
      let routed_to = 'DCA';
      if (complaintData.violation_type === 'Food Safety') routed_to = 'FSSAI';
      else if (complaintData.violation_type === 'Both') routed_to = 'Both';

      const trackingId = 'GK-' + Math.random().toString(36).substring(2, 8).toUpperCase();
      const mockComplaint = {
        id: Math.floor(Math.random() * 500) + 1,
        tracking_id: trackingId,
        shop_id: complaintData.shop_id,
        product_details: complaintData.product_details,
        violation_type: complaintData.violation_type,
        verification_method: complaintData.verification_method,
        evidence_url: complaintData.evidence_url,
        status: complaintData.verification_method !== 'None' ? 'Verified' : 'Pending',
        routed_to: routed_to,
        is_verified: complaintData.verification_method !== 'None',
        date_filed: new Date().toISOString()
      };

      // Save to localStorage for demo persistence
      const stored = JSON.parse(localStorage.getItem('gk_complaints') || '[]');
      stored.unshift(mockComplaint);
      localStorage.setItem('gk_complaints', JSON.stringify(stored));

      return mockComplaint;
    }
  },

  // 6. Track Complaint
  async getComplaint(trackingId) {
    try {
      const response = await fetch(`${CONFIG.API_BASE_URL}/api/complaints/${trackingId}`);
      if (!response.ok) throw new Error('Complaint not found');
      return await response.json();
    } catch (error) {
      const stored = JSON.parse(localStorage.getItem('gk_complaints') || '[]');
      const found = stored.find(c => c.tracking_id.toUpperCase() === trackingId.toUpperCase());
      if (found) return found;

      // Generate realistic mock for any random search
      return {
        id: 99,
        tracking_id: trackingId.toUpperCase(),
        shop_id: 1,
        product_details: 'Packaged beverage missing mandatory batch date and containing unapproved food color.',
        violation_type: 'Both',
        verification_method: 'Aadhaar QR (Zero Storage)',
        status: 'Investigation in Progress',
        routed_to: 'Both',
        is_verified: true,
        date_filed: new Date(Date.now() - 86400000 * 2).toISOString()
      };
    }
  },

  // 7. Officer Login
  async officerLogin(username, password) {
    try {
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);

      const response = await fetch(`${CONFIG.API_BASE_URL}/api/officer/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData
      });

      if (!response.ok) throw new Error('Invalid credentials');
      const data = await response.json();
      localStorage.setItem('gk_officer_token', data.access_token);
      localStorage.setItem('gk_officer_user', username);
      return data;
    } catch (error) {
      // Demo authentication simulation
      if (username === 'officer' && (password === 'password' || password === 'admin' || password === 'officer123')) {
        const mockToken = 'mock_jwt_token_' + Date.now();
        localStorage.setItem('gk_officer_token', mockToken);
        localStorage.setItem('gk_officer_user', username);
        return { access_token: mockToken, token_type: 'bearer' };
      }
      throw new Error('Invalid credentials. (Hint: Try username: "officer", password: "password")');
    }
  },

  // 8. Log Officer Inspection
  async logInspection(inspectionData) {
    const token = localStorage.getItem('gk_officer_token');
    try {
      const response = await fetch(`${CONFIG.API_BASE_URL}/api/officer/inspections`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(inspectionData)
      });
      if (!response.ok) throw new Error('Failed to log inspection');
      return await response.json();
    } catch (error) {
      const mockInspection = {
        id: Math.floor(Math.random() * 1000) + 1,
        shop_id: inspectionData.shop_id,
        product_scanned: inspectionData.product_scanned,
        is_compliant: inspectionData.is_compliant,
        violation_details: inspectionData.violation_details,
        date_logged: new Date().toISOString(),
        officer_id: 1
      };

      const stored = JSON.parse(localStorage.getItem('gk_inspections') || '[]');
      stored.unshift(mockInspection);
      localStorage.setItem('gk_inspections', JSON.stringify(stored));
      return mockInspection;
    }
  },

  // 9. Get Officer Inspections
  async getOfficerInspections() {
    const token = localStorage.getItem('gk_officer_token');
    try {
      const response = await fetch(`${CONFIG.API_BASE_URL}/api/officer/inspections`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (!response.ok) throw new Error('Failed to fetch officer inspections');
      return await response.json();
    } catch (error) {
      const stored = JSON.parse(localStorage.getItem('gk_inspections') || '[]');
      if (stored.length > 0) return stored;

      return [
        {
          id: 101,
          shop_id: 1,
          product_scanned: 'Volt Turbo Energy Drink 250ml',
          is_compliant: false,
          violation_details: 'Missing MRP declaration, Tartrazine additive violation. Offence Compounded.',
          date_logged: new Date(Date.now() - 86400000 * 1).toISOString(),
          officer_id: 1
        },
        {
          id: 102,
          shop_id: 2,
          product_scanned: 'Nutra-Natural Oat Flakes 500g',
          is_compliant: true,
          violation_details: 'All Legal Metrology and FSSAI declarations verified compliant.',
          date_logged: new Date(Date.now() - 86400000 * 3).toISOString(),
          officer_id: 1
        }
      ];
    }
  }
};

window.API = API;
