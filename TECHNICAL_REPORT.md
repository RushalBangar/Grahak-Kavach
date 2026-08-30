# Grahak Kavach - Technical Report

**Grahak Kavach** is an end-to-end web application designed to empower citizens to file complaints regarding legal metrology (MRP, expiry dates, weights) and food safety violations, while providing a powerful analytics and management dashboard for government officers.

---

## 1. System Architecture

The application is built on a decoupled Client-Server architecture:
- **Frontend**: A static, Progressive Web App (PWA) built with Vanilla web technologies to ensure maximum compatibility, fast load times, and simple hosting on **Vercel**.
- **Backend**: A RESTful API built with Python, providing high performance, asynchronous request handling, and strict data validation, deployed on **Render**.
- **Database**: A relational database model used for structured storage of users, complaints, shops, and inspection logs.

---

## 2. Technology Stack

### Frontend (Client-Side)
* **Languages**: HTML5, CSS3, Vanilla JavaScript (ES6+).
* **Styling**: Custom CSS utilizing modern **Glassmorphism** aesthetics (backdrop filters, semi-transparent overlays) and responsive design without relying on heavy frameworks like Bootstrap or Tailwind.
* **Mapping**: **Leaflet.js** for rendering interactive heatmaps on the Officer Dashboard.
* **Camera/Imaging**: WebRTC API (`getUserMedia`) for capturing label photos directly from the browser.
* **PWA**: Service Worker (`sw.js`) and Web App Manifest (`manifest.json`) for installability and offline caching.

### Backend (Server-Side)
* **Framework**: **FastAPI** (Python 3.10+). Chosen for its auto-generated Swagger documentation, asynchronous capabilities (`async/await`), and speed.
* **Server**: **Uvicorn** (ASGI server).
* **Validation**: **Pydantic** for strict request/response schema validation and type checking.
* **Authentication**: **JWT (JSON Web Tokens)** + bcrypt password hashing (via `passlib`) for secure Officer login sessions.
* **Optical Character Recognition (OCR)**: **Tesseract OCR** (`pytesseract`) + `Pillow` for extracting text from uploaded product labels.
* **External APIs**: Integrated with the **Open Food Facts API** for global barcode lookups and authenticity verification.

### Database
* **Local Development**: **SQLite** (`sql_app.db`) for rapid iteration and testing.
* **Production**: **PostgreSQL** hosted on **Supabase**.
* **ORM**: **SQLAlchemy** for mapping Python classes to database tables and preventing SQL Injection attacks.

---

## 3. Key Features Implemented

### Citizen-Facing Features
1. **Multi-Step Complaint Wizard**: A user-friendly, step-by-step form for submitting complaints with evidence (photos/receipts).
2. **Geo-Tagging**: Utilizes the browser's Geolocation API to attach exact latitude and longitude coordinates to incoming complaints.
3. **Dual Scan Modes**:
   - **Barcode Scanning**: Validates product EAN/UPC barcodes against the global Open Food Facts database to check for authenticity and ultra-processed health flags.
   - **OCR Label Scanning**: Extracts text from images to verify MRP, packaging dates, and expiry dates.
4. **Rule-Based Chatbot**: A lightweight, client-side NLP chatbot engine that assists users with Legal Metrology laws and guides them through the platform without the cost or latency of LLMs.
5. **Localization (i18n)**: Built-in dictionary support for English, Hindi, and Marathi to ensure rural and urban accessibility.

### Officer-Facing Features
1. **Secure OTP Login**: A simulated OTP-to-Email verification flow that grants a secure JWT session token.
2. **Interactive Heatmaps**: A visual representation of violation hotspots (Legal Metrology vs. Food Safety) powered by Leaflet.js, allowing officers to deploy resources efficiently.
3. **Complaint Triage & Routing**: Auto-routing backend logic that categorizes complaints for the DCA (Department of Consumer Affairs) or FSSAI.

---

## 4. Security & Compliance

To protect the platform from abuse, we implemented a **Defense in Depth** security model:

1. **API Signatures (HMAC)**:
   - The frontend generates a time-stamped HMAC SHA-256 signature using the Web Crypto API (`window.crypto.subtle`).
   - The backend validates the signature against a shared secret and enforces a strict 5-minute timeout window to prevent replay attacks and stop scripted bot traffic.
2. **Google reCAPTCHA v2**:
   - Integrated into the complaint submission and barcode verification forms to prevent automated headless browsers (like Selenium) from spamming the system.
3. **Input Validation**:
   - Strict Pydantic models on the backend reject malformed payloads, preventing NoSQL/SQL injection and XSS payload storage.
4. **Environment Isolation**:
   - Sensitive credentials (Supabase URIs, HMAC secrets, Captcha keys) are isolated in `.env` files and strictly excluded from version control via `.gitignore`.

---

*Report generated automatically for project documentation.*
