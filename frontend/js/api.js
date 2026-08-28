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

    // --- Native Backend Email OTP Flow ---
    sendOTP: async (email) => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/officer/send-otp`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: email })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to send OTP');
            }
            
            window.currentLoginEmail = email; // Save for verification step
            
            // UI transitions
            document.getElementById('step-1-form').style.display = 'none';
            document.getElementById('step-2-form').style.display = 'block';
            if(typeof showToast === 'function') { showToast("OTP Sent to " + email, "success"); } else { alert("OTP Sent to " + email); }
        } catch (error) {
            console.error("Error sending OTP", error);
            alert("Error sending OTP: " + error.message);
        }
    },

    verifyOTP: async (otp) => {
        try {
            const email = window.currentLoginEmail;
            if (!email) throw new Error("No email found for verification");

            const response = await fetch(`${API_BASE_URL}/api/officer/verify-otp`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: email, otp: otp })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Invalid OTP');
            }

            const data = await response.json();
            
            // Save token
            localStorage.setItem('officer_token', data.access_token);
            
            if(typeof showToast === 'function') { showToast("Login successful!", "success"); } else { alert("Login successful!"); }
            setTimeout(() => {
                window.location.href = 'officer-dashboard.html';
            }, 1000);
        } catch (error) {
            console.error("Error verifying OTP", error);
            alert(error.message);
        }
    },

    getComplaintsQueue: async () => {
        const response = await fetch(`${API_BASE_URL}/api/complaints/queue`);
        if (!response.ok) throw new Error('Failed to fetch queue');
        return await response.json();
    }
};

