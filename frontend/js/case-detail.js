// Case Detail Page Controller

document.addEventListener('DOMContentLoaded', async () => {
  const currentUser = await auth.requireRole(['hod', 'dean', 'higher_authority', 'administrator']);
  if (!currentUser) return;

  const urlParams = new URLSearchParams(window.location.search);
  const caseId = urlParams.get('id');
  if (!caseId) {
    window.location.href = '/dashboard.html';
    return;
  }

  // Header User Display
  const userDisplayEl = document.getElementById('userDisplayName');
  if (userDisplayEl) {
    userDisplayEl.textContent = `${currentUser.name} (${currentUser.role.toUpperCase()})`;
  }
  document.getElementById('logoutBtn')?.addEventListener('click', () => auth.logout());

  let caseData = null;

  async function loadCaseDetail() {
    try {
      caseData = await api.get(`/cases/${caseId}`);

      document.getElementById('caseRefHeading').textContent = caseData.public_reference;
      document.getElementById('caseBadge').innerHTML = renderStatusBadge(caseData.status, caseData.is_urgent);

      document.getElementById('detailCategory').textContent = `${caseData.type.toUpperCase()} • ${caseData.category}`;
      document.getElementById('detailDate').textContent = `${new Date(caseData.incident_date).toLocaleDateString()} ${caseData.incident_time ? '(' + caseData.incident_time + ')' : ''}`;
      document.getElementById('detailLocation').textContent = caseData.location_or_platform;
      document.getElementById('detailMode').textContent = caseData.reporting_mode.toUpperCase();
      document.getElementById('detailDescription').textContent = caseData.description;

      // Group Pattern & Escalation Tier Info
      const tierMap = { 1: 'Level 1: HOD', 2: 'Level 2: Dean', 3: 'Level 3: Higher Authority' };
      document.getElementById('detailTier').textContent = tierMap[caseData.current_escalation_level] || 'Level 1';
      document.getElementById('detailPatternGroup').textContent = caseData.group_reference 
        ? `${caseData.group_reference} (${caseData.confirmed_reports_in_group} confirmed reports)`
        : 'Single Independent Incident';

      // Suspect Allegations
      const suspectsContainer = document.getElementById('suspectsList');
      if (caseData.suspect_details && caseData.suspect_details.length > 0) {
        suspectsContainer.innerHTML = caseData.suspect_details.map(s => `
          <div style="background: var(--bg-surface-elevated); padding: 12px; border-radius: var(--radius-md); margin-top: 8px;">
            <strong>${s.name || 'Name not provided'}</strong>
            <span style="font-size: 0.8rem; color: var(--text-muted);"> • ${s.department || 'Dept N/A'}</span>
            ${s.other_description ? `<p style="font-size: 0.82rem; margin-top: 4px;">${s.other_description}</p>` : ''}
          </div>
        `).join('');
      } else {
        suspectsContainer.innerHTML = '<p style="color: var(--text-muted); font-size: 0.82rem;">No suspect details provided.</p>';
      }

      // Evidence list
      const evidenceContainer = document.getElementById('evidenceList');
      if (caseData.evidence_items && caseData.evidence_items.length > 0) {
        evidenceContainer.innerHTML = caseData.evidence_items.map(e => `
          <div style="display: flex; justify-content: space-between; align-items: center; background: var(--bg-surface-elevated); padding: 10px 14px; border-radius: var(--radius-md); margin-top: 8px;">
            <span>📎 <strong>${e.original_filename_display}</strong> (${(e.file_size / 1024).toFixed(1)} KB)</span>
            <button class="btn btn-sm btn-outline-primary download-evidence-btn" data-ev-id="${e.id}">Download File</button>
          </div>
        `).join('');

        document.querySelectorAll('.download-evidence-btn').forEach(btn => {
          btn.addEventListener('click', () => {
            const evId = btn.getAttribute('data-ev-id');
            window.open(`/api/evidence/${evId}`, '_blank');
          });
        });
      } else {
        evidenceContainer.innerHTML = '<p style="color: var(--text-muted); font-size: 0.82rem;">No evidence files attached.</p>';
      }

      // Identity Section
      const identitySection = document.getElementById('identityVaultSection');
      if (caseData.reporting_mode === 'anonymous') {
        identitySection.innerHTML = `
          <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: var(--radius-md); padding: 14px;">
            <strong style="color: var(--color-success);">🛡️ Anonymous Submission</strong>
            <p style="font-size: 0.82rem; margin-top: 4px;">No student identity or contact details exist in the database for this case.</p>
          </div>
        `;
      } else {
        identitySection.innerHTML = `
          <div style="background: var(--bg-surface-elevated); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <div>
                <strong>🔒 Reporter Identity Vault (Confidential Mode)</strong>
                <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 2px;">Identity is protected and query-isolated under institutional policy.</p>
              </div>
              <button class="btn btn-sm btn-urgent" id="openUnmaskModalBtn">Request Clearance</button>
            </div>
            <div id="unmaskedDataContainer" style="display: none; margin-top: 14px; padding-top: 14px; border-top: 1px solid var(--border-subtle);"></div>
          </div>
        `;

        document.getElementById('openUnmaskModalBtn')?.addEventListener('click', () => {
          openModal('unmaskModal');
        });
      }

      // Status History Timeline
      const historyContainer = document.getElementById('statusHistoryList');
      if (caseData.status_history && caseData.status_history.length > 0) {
        historyContainer.innerHTML = caseData.status_history.map(h => `
          <div style="border-left: 2px solid var(--color-primary); padding-left: 12px; margin-bottom: 12px;">
            <div style="font-size: 0.82rem; font-weight: 600; color: var(--text-primary);">${h.new_status.toUpperCase()}</div>
            <div style="font-size: 0.72rem; color: var(--text-muted);">${new Date(h.created_at).toLocaleString()}</div>
            <p style="font-size: 0.8rem; margin-top: 2px;">${h.reason || 'Status updated.'}</p>
          </div>
        `).join('');
      }

      // Set current status in dropdown
      const statusSelect = document.getElementById('newStatusSelect');
      if (statusSelect) statusSelect.value = caseData.status;

    } catch (err) {
      showToast('Error loading case detail: ' + err.message, 'error');
    }
  }

  // Update Status Form
  document.getElementById('statusUpdateForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const newStatus = document.getElementById('newStatusSelect').value;
    const reason = document.getElementById('statusReason').value.trim();
    if (!reason) {
      showToast('A documented rationale is mandatory for status updates.', 'error');
      return;
    }

    try {
      await api.patch(`/cases/${caseId}/status`, { new_status: newStatus, reason: reason });
      showToast('Case status updated successfully.', 'success');
      document.getElementById('statusReason').value = '';
      loadCaseDetail();
    } catch (err) {
      showToast(err.message, 'error');
    }
  });

  // Manual Escalation Form
  document.getElementById('manualEscalateForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const targetLevel = parseInt(document.getElementById('escalateLevelSelect').value);
    const reason = document.getElementById('escalateReason').value.trim();
    if (!reason) {
      showToast('Please provide an escalation justification.', 'error');
      return;
    }

    try {
      await api.post(`/cases/${caseId}/escalate`, { target_level: targetLevel, reason: reason });
      showToast(`Case escalated to Level ${targetLevel} successfully.`, 'success');
      document.getElementById('escalateReason').value = '';
      loadCaseDetail();
    } catch (err) {
      showToast(err.message, 'error');
    }
  });

  // Exceptional Unmask Request Form
  document.getElementById('unmaskForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const reason = document.getElementById('unmaskReason').value.trim();
    if (!reason || reason.length < 10) {
      showToast('Please provide a substantive justification (at least 10 characters).', 'error');
      return;
    }

    try {
      const identityData = await api.post(`/cases/${caseId}/request-identity`, { justified_reason: reason });
      closeModal('unmaskModal');
      showToast('Identity clearance granted. Access logged to audit trail.', 'success');

      const container = document.getElementById('unmaskedDataContainer');
      container.style.display = 'block';
      container.innerHTML = `
        <div style="background: var(--bg-input); padding: 12px; border-radius: var(--radius-sm);">
          <strong style="color: var(--color-urgent);">Unmasked Reporter Information (Audit Record Created):</strong>
          <div style="margin-top: 6px; font-size: 0.85rem;">
            <div><strong>Name:</strong> ${identityData.full_name || 'N/A'}</div>
            <div><strong>Email:</strong> ${identityData.email || 'N/A'}</div>
            <div><strong>Phone:</strong> ${identityData.phone || 'N/A'}</div>
            <div><strong>Department:</strong> ${identityData.department || 'N/A'}</div>
            <div><strong>Student ID:</strong> ${identityData.student_id_number || 'N/A'}</div>
          </div>
        </div>
      `;
    } catch (err) {
      showToast(err.message, 'error');
    }
  });

  loadCaseDetail();
});
