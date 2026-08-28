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
            '19ba44147568b058ae9051f10363fdba6055e688fe804a247ebfff8fe939bf51', // Hash for 8329810968
            '6b4a6469e5f3dedef7810a6a78b8ac6c04087e426a89fc1d7ba5bf99148cdbcf', // Hash for 7558748139
            '1757d05c1f9649e316679591815f4226e14f53e24e71a8f237c167a33ab40493', // Hash for 9552872589
            '5586146697218518d948cd5ee830db4bb4be6129d2d21924e1df24b9b45faa1d', // Hash for 8856909511
            'bcd5fff8baadc3729dd7037fec41ca6da423f22363bb69557c84afbbd33668ec', // Hash for 9673295139
            'bae5ff652da6375bb2aba60746b3945f3d4223b9ab331f5b7424184cb8a8f5fa'  // Hash for 8788804038
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
            if(typeof showToast === 'function') { showToast("OTP Sent to " + phoneNumber, "success"); } else { alert("OTP Sent to " + phoneNumber); }
        } catch (error) {
            console.error("Error sending OTP", error);
            alert("Error sending OTP: " + error.message);
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
            
            if(typeof showToast === 'function') { showToast("Login successful!", "success"); } else { alert("Login successful!"); }
            setTimeout(() => {
                window.location.href = 'officer-dashboard.html';
            }, 1000);
        } catch (error) {
            console.error("Error verifying OTP", error);
            alert("Invalid OTP entered or verification failed.");
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
