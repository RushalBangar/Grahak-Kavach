# 🛡️ Grahak Kavach (ग्राहक कवच) — Frontend Application
**Unified AI Packaged Commodity Compliance & Food Safety Platform**  
*Smart India Hackathon 2026 (Track: Student Innovation — SIH26197)*

---

## 🌟 Overview
This frontend provides a complete, modern web interface for the **Grahak Kavach** platform. It allows consumers and enforcement officers to:
1. **AI Label Scanner**: Scan any packaged commodity label to verify **Legal Metrology (2011 Rules)** and **Food Safety (FSSAI 2020 Regulations)** from a single image.
2. **Nutri-Score & Harmful Additives Radar**: Instant visual health grade (A through E) and detection of hazardous chemicals (*Tartrazine, MSG, High Fructose Corn Syrup, Aspartame*).
3. **DPDP Act 2023 Compliant Complaint Wizard**: File evidence-backed consumer grievances with zero Aadhaar number storage via offline digital signature validation.
4. **Smart Multi-Dept Auto-Routing**: Automatically directs complaints to the **Department of Consumer Affairs (DCA)**, **FSSAI**, or splits dual violations simultaneously.
5. **Real-Time Grievance Tracker**: Public tracking ledger with live status timelines.
6. **Shop Compliance Ledger**: Citizen lookup for local shop inspection records and trust scores.
7. **Officer Enforcement Portal**: Secure JWT authentication, zonal compliance metrics, and inspection logging.

---

## 🏗️ Technology Stack
- **Structure**: Semantic HTML5 (Single-Page Application architecture)
- **Styling**: Modern Vanilla CSS3 (Glassmorphism, Dark/Light theme, responsive grid, micro-animations)
- **Logic**: Modular Vanilla JavaScript (ES6+ standard)
- **API Integration**: REST API connection to FastAPI backend with automatic hybrid offline fallback simulation

---

## 📁 Directory Structure
```
frontend/
├── index.html              # Main SPA container with 6 dynamic views & modals
├── css/
│   ├── style.css           # Core design system, theme variables, glassmorphism, responsive grid
│   ├── scanner.css         # Laser scanner animation, Nutri-Score gauge, checklist styles
│   ├── complaints.css      # DPDP 2023 banner, verification tiers, tracking timeline
│   └── officer.css         # Officer enforcement suite, metrics cards, inspection logbook
├── js/
│   ├── config.js           # API endpoints & judge pitch sample presets
│   ├── api.js              # FastAPI client with hybrid offline simulation fallback
│   ├── scanner.js          # Label image capture, live camera, preset loaders & result visualizer
│   ├── complaints.js       # DPDP verification modals, complaint wizard, tracking engine
│   ├── shops.js            # Shop search & compliance trust index explorer
│   ├── officer.js          # Officer JWT login, metric counters, inspection logging
│   └── app.js              # SPA navigation, theme toggle, toast notifications
└── README.md
```

---

## 🚀 How to Run

### Option 1: Standalone Frontend
Open `index.html` directly in any modern web browser, or serve it using Python:
```bash
python -m http.server 3000 --directory frontend
```
Visit: `http://localhost:3000`

### Option 2: Full-Stack (with Backend)
1. Start the FastAPI backend:
   ```bash
   cd backend
   uvicorn main:app --reload --port 8000
   ```
2. Start the frontend:
   ```bash
   python -m http.server 3000 --directory frontend
   ```
The frontend will detect port 8000 and display **"Backend Live (Port 8000)"** in the top navigation.
