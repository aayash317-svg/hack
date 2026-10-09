// Related-Case Match Review Controller (Section 23 Implementation)

document.addEventListener('DOMContentLoaded', async () => {
  const currentUser = await auth.requireRole(['hod', 'dean', 'higher_authority', 'administrator']);
  if (!currentUser) return;

  const userDisplayEl = document.getElementById('userDisplayName');
  if (userDisplayEl) {
    userDisplayEl.textContent = `${currentUser.name} (${currentUser.role.toUpperCase()})`;
  }
  document.getElementById('logoutBtn')?.addEventListener('click', () => auth.logout());

  const reviewQueueContainer = document.getElementById('reviewQueueContainer');
  const emptyState = document.getElementById('reviewEmptyState');

  let activeLinkId = null;
  let activeDecision = null;

  async function loadPendingReviews() {
    try {
      const items = await api.get('/authority/match-reviews');
      reviewQueueContainer.innerHTML = '';

      if (items.length === 0) {
        emptyState.style.display = 'block';
        return;
      }

      emptyState.style.display = 'none';

      items.forEach(item => {
        const card = document.createElement('div');
        card.className = 'card';
        card.style.marginBottom = '24px';

        card.innerHTML = `
          <div class="card-header">
            <div>
              <span class="badge badge-review"><span class="badge-dot"></span>Candidate Match Proposal</span>
              <span style="font-size: 0.8rem; color: var(--text-muted); margin-left: 10px;">Flagged: ${new Date(item.created_at).toLocaleString()}</span>
            </div>
          </div>

          <div style="margin-bottom: 16px;">
            <strong style="font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase;">Matched Attributes:</strong>
            <div class="feature-tag-list">
              ${item.matched_features.map(f => `<span class="feature-tag">${f}</span>`).join('')}
            </div>
          </div>

          <div class="review-matrix">
            <div class="review-candidate-card">
              <div class="candidate-header">
                <div>
                  <strong class="font-mono" style="color: var(--color-primary);">${item.complaint_a.public_reference}</strong>
                  <span style="font-size: 0.78rem; color: var(--text-muted); display: block;">Report A</span>
                </div>
                <span class="badge badge-submitted">${item.complaint_a.category}</span>
              </div>
              <p><strong>Type:</strong> ${item.complaint_a.type.toUpperCase()}</p>
              <p><strong>Date:</strong> ${new Date(item.complaint_a.incident_date).toLocaleDateString()}</p>
              <p><strong>Location:</strong> ${item.complaint_a.location_or_platform}</p>
              <p style="margin-top: 8px;"><strong>Narrative:</strong> ${item.complaint_a.description}</p>
              ${item.complaint_a.suspect_summary ? `<p style="margin-top: 6px; font-size: 0.8rem; color: var(--color-warning);"><strong>Suspect Allegation:</strong> ${item.complaint_a.suspect_summary}</p>` : ''}
            </div>

            <div class="review-candidate-card">
              <div class="candidate-header">
                <div>
                  <strong class="font-mono" style="color: var(--color-primary);">${item.complaint_b.public_reference}</strong>
                  <span style="font-size: 0.78rem; color: var(--text-muted); display: block;">Report B</span>
                </div>
                <span class="badge badge-submitted">${item.complaint_b.category}</span>
              </div>
              <p><strong>Type:</strong> ${item.complaint_b.type.toUpperCase()}</p>
              <p><strong>Date:</strong> ${new Date(item.complaint_b.incident_date).toLocaleDateString()}</p>
              <p><strong>Location:</strong> ${item.complaint_b.location_or_platform}</p>
              <p style="margin-top: 8px;"><strong>Narrative:</strong> ${item.complaint_b.description}</p>
              ${item.complaint_b.suspect_summary ? `<p style="margin-top: 6px; font-size: 0.8rem; color: var(--color-warning);"><strong>Suspect Allegation:</strong> ${item.complaint_b.suspect_summary}</p>` : ''}
            </div>
          </div>

          <div style="display: flex; gap: 12px; justify-content: flex-end; padding-top: 14px; border-top: 1px solid var(--border-subtle);">
            <button class="btn btn-secondary action-review-btn" data-link-id="${item.link_id}" data-decision="needs_more_review">
              Defer / Need More Info
            </button>
            <button class="btn btn-urgent action-review-btn" data-link-id="${item.link_id}" data-decision="reject">
              Reject Match (Independent Incidents)
            </button>
            <button class="btn btn-primary action-review-btn" data-link-id="${item.link_id}" data-decision="confirm">
              Confirm Related Pattern
            </button>
          </div>
        `;
        reviewQueueContainer.appendChild(card);
      });

      // Hook action buttons
      document.querySelectorAll('.action-review-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          activeLinkId = btn.getAttribute('data-link-id');
          activeDecision = btn.getAttribute('data-decision');

          const titleEl = document.getElementById('decisionModalTitle');
          const descEl = document.getElementById('decisionModalDesc');
          const submitBtn = document.getElementById('confirmDecisionBtn');

          if (activeDecision === 'confirm') {
            titleEl.textContent = 'Confirm Related Incident Pattern';
            descEl.textContent = 'Per Section 23 policy, confirming this link consolidates these reports into a verified case group and evaluates progressive escalation (Level 1 HOD -> Level 2 Dean -> Level 3 Higher Authority).';
            submitBtn.className = 'btn btn-primary';
            submitBtn.textContent = 'Confirm & Recalculate Escalation';
          } else if (activeDecision === 'reject') {
            titleEl.textContent = 'Reject Candidate Match';
            descEl.textContent = 'Per Section 23 policy, rejecting marks these complaints as separate incidents. The repeat-report count will NOT be incremented.';
            submitBtn.className = 'btn btn-urgent';
            submitBtn.textContent = 'Confirm Rejection';
          } else {
            titleEl.textContent = 'Defer Match Decision';
            descEl.textContent = 'Mark this link as requiring further investigation before a relationship can be confirmed or rejected.';
            submitBtn.className = 'btn btn-secondary';
            submitBtn.textContent = 'Defer Match';
          }

          document.getElementById('decisionReasonInput').value = '';
          openModal('decisionModal');
        });
      });

    } catch (err) {
      showToast('Error loading match reviews: ' + err.message, 'error');
    }
  }

  // Submit Decision Form
  document.getElementById('decisionForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const reason = document.getElementById('decisionReasonInput').value.trim();
    if (!reason || reason.length < 3) {
      showToast('A documented rationale is mandatory for review decisions.', 'error');
      return;
    }

    try {
      await api.post(`/cases/match-reviews/${activeLinkId}/decide`, {
        decision: activeDecision,
        reason: reason
      });
      closeModal('decisionModal');
      showToast('Review decision recorded successfully.', 'success');
      loadPendingReviews();
    } catch (err) {
      showToast(err.message, 'error');
    }
  });

  loadPendingReviews();
});
