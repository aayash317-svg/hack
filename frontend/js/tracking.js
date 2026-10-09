// Tracking Page Controller

document.addEventListener('DOMContentLoaded', () => {
  const trackForm = document.getElementById('trackForm');
  const trackBtn = document.getElementById('trackBtn');
  const refInput = document.getElementById('refInput');
  const secretInput = document.getElementById('secretInput');
  const resultsContainer = document.getElementById('trackingResults');
  const autofillBanner = document.getElementById('autofillBanner');
  const toggleSecretBtn = document.getElementById('toggleSecretBtn');

  // Toggle secret visibility
  if (toggleSecretBtn && secretInput) {
    toggleSecretBtn.addEventListener('click', () => {
      if (secretInput.type === 'password') {
        secretInput.type = 'text';
        toggleSecretBtn.textContent = 'Hide Secret';
      } else {
        secretInput.type = 'password';
        toggleSecretBtn.textContent = 'Show Secret';
      }
    });
  }

  // Auto-populate from URL query params or sessionStorage fallback
  const urlParams = new URLSearchParams(window.location.search);
  const paramRef = (urlParams.get('ref') || sessionStorage.getItem('last_track_ref') || '').trim();
  const paramSec = (urlParams.get('sec') || sessionStorage.getItem('last_track_sec') || '').trim();

  if (paramRef && refInput) refInput.value = paramRef;
  if (paramSec && secretInput) secretInput.value = paramSec;

  if (paramRef && paramSec) {
    if (autofillBanner) autofillBanner.style.display = 'block';
    executeTracking(paramRef, paramSec);
  }

  trackForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const ref = refInput.value.trim();
    const secret = secretInput.value.trim();
    if (!ref || !secret) {
      showToast('Please enter both the reference code and tracking secret.', 'error');
      return;
    }
    executeTracking(ref, secret);
  });

  async function executeTracking(ref, secret) {
    trackBtn.disabled = true;
    trackBtn.textContent = 'Verifying credentials...';

    try {
      const data = await api.get('/complaints/track', { reference: ref, secret: secret });

      resultsContainer.style.display = 'block';
      resultsContainer.scrollIntoView({ behavior: 'smooth' });

      document.getElementById('resReference').textContent = data.public_reference;
      document.getElementById('resMode').textContent = data.reporting_mode.toUpperCase();
      document.getElementById('resCategory').textContent = `${data.type.toUpperCase()} • ${data.category}`;
      document.getElementById('resDate').textContent = new Date(data.incident_date).toLocaleDateString();
      document.getElementById('resBadge').innerHTML = renderStatusBadge(data.status, data.is_urgent);
      document.getElementById('resPublicMessage').textContent = data.public_message;

      // Render Milestone Stepper
      const stepperEl = document.getElementById('timelineStepper');
      stepperEl.innerHTML = '';

      data.timeline.forEach((item, idx) => {
        const stepEl = document.createElement('div');
        stepEl.className = `step-item ${idx === data.timeline.length - 1 ? 'active' : 'completed'}`;
        stepEl.innerHTML = `
          <div class="step-dot">${idx + 1}</div>
          <div class="step-content">
            <h4>${item.label}</h4>
            <div class="step-date">${new Date(item.timestamp).toLocaleString()}</div>
            <p>${item.description}</p>
          </div>
        `;
        stepperEl.appendChild(stepEl);
      });

    } catch (err) {
      showToast(err.message || 'Verification failed. Please check credentials.', 'error');
    } finally {
      trackBtn.disabled = false;
      trackBtn.textContent = 'Check Case Status';
    }
  }
});
