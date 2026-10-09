// UI Helper Components & Toast Manager

function showToast(message, type = 'info') {
  let container = document.getElementById('toastContainer');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.setAttribute('role', 'alert');

  const iconMap = {
    success: '✔',
    error: '✖',
    info: 'ℹ'
  };

  toast.innerHTML = `
    <span style="font-weight: bold; color: ${type === 'error' ? 'var(--color-urgent)' : type === 'success' ? 'var(--color-success)' : 'var(--color-primary)'}">
      ${iconMap[type] || '•'}
    </span>
    <span style="flex: 1;">${message}</span>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    toast.style.transition = 'all 200ms ease-in';
    setTimeout(() => toast.remove(), 250);
  }, 4000);
}

function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove('active');
    document.body.style.overflow = '';
  }
}

// Global modal overlay click and escape listener
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal-overlay.active').forEach(m => m.classList.remove('active'));
    document.body.style.overflow = '';
  }
});

function copyToClipboard(text, successMsg = 'Copied to clipboard!') {
  if (navigator.clipboard) {
    navigator.clipboard.writeText(text).then(() => {
      showToast(successMsg, 'success');
    }).catch(() => {
      fallbackCopy(text, successMsg);
    });
  } else {
    fallbackCopy(text, successMsg);
  }
}

function fallbackCopy(text, successMsg) {
  const input = document.createElement('input');
  input.value = text;
  document.body.appendChild(input);
  input.select();
  document.execCommand('copy');
  document.body.removeChild(input);
  showToast(successMsg, 'success');
}

function renderStatusBadge(status, isUrgent = false) {
  if (isUrgent) {
    return `<span class="badge badge-urgent"><span class="badge-dot"></span>Urgent Alert</span>`;
  }
  const map = {
    submitted: { cls: 'badge-submitted', text: 'Submitted' },
    under_review: { cls: 'badge-review', text: 'Under Review' },
    pending_match_review: { cls: 'badge-review', text: 'Pattern Review' },
    escalated: { cls: 'badge-escalated', text: 'Escalated' },
    resolved: { cls: 'badge-resolved', text: 'Resolved' },
    closed: { cls: 'badge-secondary', text: 'Closed' }
  };
  const b = map[status] || { cls: 'badge-submitted', text: status };
  return `<span class="badge ${b.cls}"><span class="badge-dot"></span>${b.text}</span>`;
}
