// Authority Dashboard Controller

document.addEventListener('DOMContentLoaded', async () => {
  const currentUser = await auth.requireRole(['hod', 'dean', 'higher_authority', 'administrator']);
  if (!currentUser) return;

  // Header User Display
  const userDisplayEl = document.getElementById('userDisplayName');
  if (userDisplayEl) {
    userDisplayEl.textContent = `${currentUser.name} (${currentUser.role.toUpperCase()})`;
  }

  // Logout button
  document.getElementById('logoutBtn')?.addEventListener('click', () => auth.logout());

  let allCases = [];
  const tableBody = document.getElementById('casesTableBody');
  const searchInput = document.getElementById('searchInput');
  const filterButtons = document.querySelectorAll('.filter-btn');

  let activeFilter = 'all';

  async function loadDashboardData() {
    try {
      allCases = await api.get('/cases');

      // Update KPI metrics
      const totalCount = allCases.length;
      const urgentCount = allCases.filter(c => c.is_urgent).length;
      const pendingMatchCount = allCases.filter(c => c.status === 'pending_match_review').length;
      const escalatedCount = allCases.filter(c => c.status === 'escalated').length;

      document.getElementById('metricTotal').textContent = totalCount;
      document.getElementById('metricUrgent').textContent = urgentCount;
      document.getElementById('metricPendingMatch').textContent = pendingMatchCount;
      document.getElementById('metricEscalated').textContent = escalatedCount;

      renderFilteredCases();
    } catch (err) {
      showToast('Error loading case queue: ' + err.message, 'error');
    }
  }

  function renderFilteredCases() {
    const searchTerm = (searchInput?.value || '').toLowerCase().trim();

    let filtered = allCases.filter(c => {
      // Status & category filter
      if (activeFilter === 'urgent' && !c.is_urgent) return false;
      if (activeFilter === 'pending' && c.status !== 'pending_match_review') return false;
      if (activeFilter === 'escalated' && c.status !== 'escalated') return false;
      if (activeFilter === 'under_review' && c.status !== 'under_review') return false;

      // Search term filter
      if (searchTerm) {
        const matchRef = c.public_reference.toLowerCase().includes(searchTerm);
        const matchCat = c.category.toLowerCase().includes(searchTerm);
        const matchLoc = c.location_or_platform.toLowerCase().includes(searchTerm);
        return matchRef || matchCat || matchLoc;
      }
      return true;
    });

    tableBody.innerHTML = '';
    if (filtered.length === 0) {
      tableBody.innerHTML = `
        <tr>
          <td colspan="7" style="text-align: center; padding: 40px; color: var(--text-muted);">
            No cases match the selected filter.
          </td>
        </tr>
      `;
      return;
    }

    filtered.forEach(c => {
      const tr = document.createElement('tr');
      if (c.is_urgent) tr.classList.add('urgent-row');

      const patternBadge = c.case_group_id 
        ? `<span class="badge badge-escalated">${c.group_reference || 'Group'} (${c.confirmed_reports_in_group} reports)</span>`
        : `<span style="color: var(--text-muted); font-size: 0.8rem;">Independent</span>`;

      tr.innerHTML = `
        <td><strong class="font-mono" style="color: var(--color-primary);">${c.public_reference}</strong></td>
        <td>
          <span style="font-weight: 500; color: var(--text-primary);">${c.category}</span>
          <br><span style="font-size: 0.75rem; color: var(--text-muted);">${c.type.toUpperCase()} • ${c.location_or_platform}</span>
        </td>
        <td>${new Date(c.incident_date).toLocaleDateString()}</td>
        <td>${renderStatusBadge(c.status, c.is_urgent)}</td>
        <td>${patternBadge}</td>
        <td><span style="text-transform: capitalize; font-size: 0.8rem;">${c.reporting_mode}</span></td>
        <td>
          <a href="/case-detail.html?id=${c.id}" class="btn btn-sm btn-outline-primary">View Case</a>
        </td>
      `;
      tableBody.appendChild(tr);
    });
  }

  // Filter clicks
  filterButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      filterButtons.forEach(b => b.classList.remove('btn-primary'));
      filterButtons.forEach(b => b.classList.add('btn-secondary'));
      btn.classList.remove('btn-secondary');
      btn.classList.add('btn-primary');
      activeFilter = btn.getAttribute('data-filter');
      renderFilteredCases();
    });
  });

  searchInput?.addEventListener('input', () => renderFilteredCases());

  loadDashboardData();
});
