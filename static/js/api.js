const API_URL = '/api';

const api = {
    async request(url, options = {}) {
        const token = localStorage.getItem('access_token');
        const headers = {
            ...options.headers,
        };

        if (!(options.body instanceof FormData)) {
            headers['Content-Type'] = 'application/json';
        }

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(url, { ...options, headers });

        if (response.status === 401 && token) {
            // Basic refresh logic or logout
            localStorage.removeItem('access_token');
            window.location.href = '/';
        }

        return response;
    },

    async login(username, password) {
        try {
            const res = await fetch(`/api/token/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            const data = await res.json().catch(() => ({}));
            if (res.ok && data.access) {
                localStorage.setItem('access_token', data.access);
                localStorage.setItem('refresh_token', data.refresh || '');
                return { ok: true };
            }
            const msg = data.detail || data.message || (typeof data === 'string' ? data : 'Invalid username or password');
            return { ok: false, error: msg };
        } catch (err) {
            return { ok: false, error: 'Network error. Please try again.' };
        }
    },

    logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/';
    }
};

function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast toast-${type} animate-fade`;
    toast.innerText = message;

    // Quick inline style for toast
    Object.assign(toast.style, {
        padding: '1rem 1.5rem',
        borderRadius: '12px',
        background: '#ffffff',
        boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
        borderLeft: `4px solid ${type === 'success' ? '#10b981' : '#4f46e5'}`,
        marginTop: '1rem',
        fontWeight: '600'
    });

    container.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}
