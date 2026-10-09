// Centralized API Client
const API_BASE = '/api';

const api = {
  getToken() {
    return localStorage.getItem('access_token');
  },

  setToken(token) {
    if (token) {
      localStorage.setItem('access_token', token);
    } else {
      localStorage.removeItem('access_token');
    }
  },

  async request(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const headers = options.headers || {};

    const token = this.getToken();
    if (token && !headers['Authorization']) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    if (!(options.body instanceof FormData) && !headers['Content-Type']) {
      headers['Content-Type'] = 'application/json';
    }

    const config = {
      ...options,
      headers,
      credentials: 'include'
    };

    try {
      const response = await fetch(url, config);
      const isJson = (response.headers.get('content-type') || '').includes('application/json');
      const data = isJson ? await response.json() : await response.text();

      if (!response.ok) {
        const errorMsg = (data && data.detail) || response.statusText || 'Request failed';
        throw new Error(errorMsg);
      }

      return data;
    } catch (err) {
      console.error(`API Error on ${endpoint}:`, err);
      throw err;
    }
  },

  get(endpoint, params = {}) {
    const qs = new URLSearchParams(params).toString();
    const path = qs ? `${endpoint}?${qs}` : endpoint;
    return this.request(path, { method: 'GET' });
  },

  post(endpoint, body) {
    const payload = body instanceof FormData ? body : JSON.stringify(body);
    return this.request(endpoint, { method: 'POST', body: payload });
  },

  patch(endpoint, body) {
    return this.request(endpoint, { method: 'PATCH', body: JSON.stringify(body) });
  }
};
