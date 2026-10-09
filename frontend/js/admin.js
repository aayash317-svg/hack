// Administrator & Audit Trail Controller

document.addEventListener('DOMContentLoaded', async () => {
  const currentUser = await auth.requireRole(['administrator']);
  if (!currentUser) return;

  const userDisplayEl = document.getElementById('userDisplayName');
  if (userDisplayEl) {
    userDisplayEl.textContent = `${currentUser.name} (ADMIN)`;
  }
  document.getElementById('logoutBtn')?.addEventListener('click', () => auth.logout());

  const usersTableBody = document.getElementById('usersTableBody');
  const auditTableBody = document.getElementById('auditTableBody');

  // Load Accounts
  async function loadUsers() {
    try {
      const users = await api.get('/admin/users');
      usersTableBody.innerHTML = '';
      users.forEach(u => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><strong>${u.name}</strong></td>
          <td>${u.email}</td>
          <td><span class="badge badge-submitted">${u.role.toUpperCase()}</span></td>
          <td>${u.department || 'N/A'}</td>
          <td>
            <span class="badge ${u.is_active ? 'badge-resolved' : 'badge-secondary'}">
              ${u.is_active ? 'Active' : 'Disabled'}
            </span>
          </td>
          <td>
            <button class="btn btn-sm btn-secondary toggle-user-btn" data-user-id="${u.id}">
              ${u.is_active ? 'Disable' : 'Enable'}
            </button>
          </td>
        `;
        usersTableBody.appendChild(tr);
      });

      document.querySelectorAll('.toggle-user-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
          const uId = btn.getAttribute('data-user-id');
          try {
            await api.patch(`/admin/users/${uId}/toggle`, {});
            showToast('Account status updated.', 'success');
            loadUsers();
          } catch (err) {
            showToast(err.message, 'error');
          }
        });
      });
    } catch (err) {
      showToast('Error loading accounts: ' + err.message, 'error');
    }
  }

  // Load Audit Trail
  async function loadAuditLogs() {
    try {
      const logs = await api.get('/admin/audit-logs');
      auditTableBody.innerHTML = '';
      logs.forEach(l => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><span class="font-mono" style="color: var(--color-primary);">${l.action}</span></td>
          <td>${l.resource_type}:${l.resource_id}</td>
          <td>${l.actor_user_id ? 'User #' + l.actor_user_id : 'System / Guest'}</td>
          <td style="max-width: 300px; word-break: break-word;">${l.reason || '—'}</td>
          <td>${l.ip_address || '—'}</td>
          <td style="white-space: nowrap;">${new Date(l.timestamp).toLocaleString()}</td>
        `;
        auditTableBody.appendChild(tr);
      });
    } catch (err) {
      showToast('Error loading audit trail: ' + err.message, 'error');
    }
  }

  // New User Form
  document.getElementById('createUserForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
      name: document.getElementById('userName').value.trim(),
      email: document.getElementById('userEmail').value.trim(),
      password: document.getElementById('userPassword').value,
      role: document.getElementById('userRole').value,
      department: document.getElementById('userDept').value.trim() || null
    };

    try {
      await api.post('/admin/users', payload);
      closeModal('createUserModal');
      showToast('New authority account created.', 'success');
      document.getElementById('createUserForm').reset();
      loadUsers();
    } catch (err) {
      showToast(err.message, 'error');
    }
  });

  document.getElementById('openCreateUserModalBtn')?.addEventListener('click', () => {
    openModal('createUserModal');
  });

  loadUsers();
  loadAuditLogs();
});
