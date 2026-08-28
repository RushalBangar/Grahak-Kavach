// api.js
const API_BASE_URL = 'https://grahak-kavach-26.onrender.com';

const API = {
    scan: async (imageFile) => {
        const formData = new FormData();
        formData.append('file', imageFile);

        const response = await fetch(`${API_BASE_URL}/api/scan/analyze`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) throw new Error('Scan failed');
        return await response.json();
    },

    submitComplaint: async (complaintData) => {
        const response = await fetch(`${API_BASE_URL}/api/complaints/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(complaintData),
        });

        if (!response.ok) throw new Error('Complaint submission failed');
        return await response.json();
    },

    searchShops: async (query) => {
        const response = await fetch(`${API_BASE_URL}/api/shops/search?query=${encodeURIComponent(query)}`);
        if (!response.ok) throw new Error('Shop search failed');
        return await response.json();
    },

    officerLogin: async (username, password) => {
        // Kept for fallback / legacy
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        const response = await fetch(`${API_BASE_URL}/api/officer/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData,
        });

        if (!response.ok) throw new Error('Login failed');
        return await response.json();
    },

    // --- Firebase OTP Auth Flow ---
    hashPhoneNumber: async (phone) => {
        const encoder = new TextEncoder();
        const data = encoder.encode(phone);
        const hashBuffer = await crypto.subtle.digest('SHA-256', data);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    },

    sendOTP: async (phoneNumber) => {
        // List of authorized officer phone numbers (SHA-256 Hashes)
        // This ensures actual phone numbers are NOT leaked in the frontend code.
        const AUTHORIZED_OFFICERS_HASHES = [
            'f3a47ce5ce3d4ca8ad15225a245b2759022f79489f5c62719b8c9490f7aab90e' // Hash for +919876543210
            // TODO: To add a new officer, compute the SHA-256 hash of their number (e.g. "+91XXXXXXXXXX") and add it here.
        ];

        const inputHash = await API.hashPhoneNumber(phoneNumber);

        if (!AUTHORIZED_OFFICERS_HASHES.includes(inputHash)) {
            alert("Unauthorized Access. This number is not registered as an officer.");
            throw new Error("Unauthorized phone number");
        }

        if (!window.recaptchaVerifier) {
            // Initialize invisible recaptcha
            window.recaptchaVerifier = new firebase.auth.RecaptchaVerifier('recaptcha-container', {
                'size': 'invisible',
                'callback': (response) => {
                    // reCAPTCHA solved
                }
            });
        }
        
        try {
            const confirmationResult = await firebase.auth().signInWithPhoneNumber(phoneNumber, window.recaptchaVerifier);
            window.confirmationResult = confirmationResult;
            
            // UI transitions
            document.getElementById('step-1-form').style.display = 'none';
            document.getElementById('step-2-form').style.display = 'block';
            if(typeof showToast === 'function') showToast("OTP Sent to " + phoneNumber, "success");
        } catch (error) {
            console.error("Error sending OTP", error);
            if(typeof showToast === 'function') showToast("Failed to send OTP. Please try again.", "error");
            if (window.recaptchaVerifier) window.recaptchaVerifier.render().then(widgetId => grecaptcha.reset(widgetId));
        }
    },

    verifyOTP: async (otp) => {
        try {
            const result = await window.confirmationResult.confirm(otp);
            const user = result.user;
            
            // Get Firebase ID token to use as officer token
            const token = await user.getIdToken();
            localStorage.setItem('officer_token', token);
            
            if(typeof showToast === 'function') showToast("Login successful!", "success");
            setTimeout(() => {
                window.location.href = 'officer-dashboard.html';
            }, 1000);
        } catch (error) {
            console.error("Error verifying OTP", error);
            if(typeof showToast === 'function') showToast("Invalid OTP entered.", "error");
        }
    },

    getComplaintsQueue: async () => {
        const response = await fetch(`${API_BASE_URL}/api/complaints/queue`);
        if (!response.ok) throw new Error('Failed to fetch queue');
        return await response.json();
    }
};

// Initialize Firebase if included on the page
if (typeof firebase !== 'undefined') {
    const firebaseConfig = {
      apiKey: "AIzaSyCQD0e3s09RJ7_MgXytRYb18uxomHkoZZc",
      authDomain: "grahak-kavach.firebaseapp.com",
      projectId: "grahak-kavach",
      storageBucket: "grahak-kavach.firebasestorage.app",
      messagingSenderId: "975024396204",
      appId: "1:975024396204:web:e11c7858eb3aac5c6d8c09",
      measurementId: "G-Z08C4BB73D"
    };
    if (!firebase.apps.length) {
        firebase.initializeApp(firebaseConfig);
    }
}
