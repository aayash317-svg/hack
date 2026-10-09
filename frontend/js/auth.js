// Authentication & Session Guard

const auth = {
  async getCurrentUser() {
    try {
      const user = await api.get('/auth/me');
      return user;
    } catch (err) {
      return null;
    }
  },

  async login(email, password) {
    const data = await api.post('/auth/login', { email, password });
    if (data.access_token) {
      api.setToken(data.access_token);
    }
    return data;
  },

  async logout() {
    try {
      await api.post('/auth/logout', {});
    } catch (e) {}
    api.setToken(null);
    window.location.href = '/login.html';
  },

  async requireRole(allowedRoles = []) {
    const user = await this.getCurrentUser();
    if (!user) {
      window.location.href = `/login.html?redirect=${encodeURIComponent(window.location.pathname)}`;
      return null;
    }
    if (allowedRoles.length > 0 && !allowedRoles.includes(user.role)) {
      showToast(`Access denied. Role ${user.role} is not permitted here.`, 'error');
      setTimeout(() => {
        window.location.href = '/dashboard.html';
      }, 1500);
      return null;
    }
    return user;
  }
};
