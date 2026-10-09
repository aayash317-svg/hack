// Complaint Submission Page Controller

document.addEventListener('DOMContentLoaded', () => {
  let selectedMode = 'anonymous';
  let selectedType = 'offline';
  let selectedFile = null;

  const modeCards = document.querySelectorAll('[data-mode]');
  const typeCards = document.querySelectorAll('[data-type]');
  const confidentialFields = document.getElementById('confidentialFields');
  const categorySelect = document.getElementById('categorySelect');
  const dropzone = document.getElementById('dropzone');
  const fileInput = document.getElementById('fileInput');
  const filePreview = document.getElementById('filePreview');
  const reportForm = document.getElementById('reportForm');
  const submitBtn = document.getElementById('submitBtn');

  // Categories by incident type
  const categories = {
    offline: [
      "Following or stalking",
      "Physical or verbal harassment",
      "Hostel intimidation or coercion",
      "Threats or intimidation",
      "Other in-person incident"
    ],
    online: [
      "Fake accounts or impersonation",
      "Obscene or abusive content",
      "Online threats or cyberbullying",
      "Unconsented photo/video sharing",
      "Other digital/online incident"
    ]
  };

  function updateCategories() {
    categorySelect.innerHTML = '<option value="">Select a specific category...</option>';
    categories[selectedType].forEach(cat => {
      const opt = document.createElement('option');
      opt.value = cat;
      opt.textContent = cat;
      categorySelect.appendChild(opt);
    });
  }
  updateCategories();

  // Mode Selection
  modeCards.forEach(card => {
    card.addEventListener('click', () => {
      modeCards.forEach(c => c.classList.remove('selected'));
      card.classList.add('selected');
      selectedMode = card.getAttribute('data-mode');

      if (selectedMode === 'confidential') {
        confidentialFields.style.display = 'block';
      } else {
        confidentialFields.style.display = 'none';
      }
    });
  });

  // Incident Type Selection
  typeCards.forEach(card => {
    card.addEventListener('click', () => {
      typeCards.forEach(c => c.classList.remove('selected'));
      card.classList.add('selected');
      selectedType = card.getAttribute('data-type');
      updateCategories();
    });
  });

  // Drag and Drop File Handlers
  if (dropzone && fileInput) {
    dropzone.addEventListener('click', () => fileInput.click());

    ['dragenter', 'dragover'].forEach(eventName => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropzone.classList.add('dragover');
      });
    });

    ['dragleave', 'drop'].forEach(eventName => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropzone.classList.remove('dragover');
      });
    });

    dropzone.addEventListener('drop', (e) => {
      const files = e.dataTransfer.files;
      if (files.length > 0) handleFile(files[0]);
    });

    fileInput.addEventListener('change', () => {
      if (fileInput.files.length > 0) handleFile(fileInput.files[0]);
    });
  }

  function handleFile(file) {
    if (file.size > 5 * 1024 * 1024) {
      showToast('File exceeds 5MB size limit.', 'error');
      return;
    }
    const allowed = ['image/png', 'image/jpeg', 'image/jpg', 'application/pdf'];
    if (!allowed.includes(file.type)) {
      showToast('Only PNG, JPG, and PDF files are accepted.', 'error');
      return;
    }
    selectedFile = file;
    filePreview.style.display = 'flex';
    filePreview.innerHTML = `
      <span>📎 <strong>${file.name}</strong> (${(file.size / 1024).toFixed(1)} KB)</span>
      <button type="button" class="btn btn-sm btn-secondary" id="removeFileBtn">Remove</button>
    `;
    document.getElementById('removeFileBtn').addEventListener('click', () => {
      selectedFile = null;
      fileInput.value = '';
      filePreview.style.display = 'none';
    });
  }

  // Form Submission
  reportForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    submitBtn.disabled = true;
    submitBtn.textContent = 'Submitting report securely...';

    const payload = {
      reporting_mode: selectedMode,
      type: selectedType,
      category: categorySelect.value,
      incident_date: document.getElementById('incidentDate').value,
      incident_time: document.getElementById('incidentTime').value || null,
      location_or_platform: document.getElementById('locationInput').value,
      description: document.getElementById('descriptionInput').value,
      is_urgent: document.getElementById('urgentCheckbox').checked
    };

    if (selectedMode === 'confidential') {
      payload.reporter_identity = {
        full_name: document.getElementById('reporterName').value || null,
        email: document.getElementById('reporterEmail').value || null,
        phone: document.getElementById('reporterPhone').value || null,
        department: document.getElementById('reporterDept').value || null,
        student_id_number: document.getElementById('reporterId').value || null
      };
    }

    const suspectName = document.getElementById('suspectName').value;
    const suspectDept = document.getElementById('suspectDept').value;
    const suspectDesc = document.getElementById('suspectDesc').value;
    if (suspectName || suspectDept || suspectDesc) {
      payload.suspect_details = [{
        name: suspectName || null,
        department: suspectDept || null,
        other_description: suspectDesc || null
      }];
    }

    try {
      const result = await api.post('/complaints', payload);

      // Upload file if selected
      if (selectedFile && result.public_reference) {
        try {
          // Look up complaint id to attach evidence
          const cases = await api.get('/cases', { status: 'submitted' }).catch(() => []);
          const createdCase = cases.find(c => c.public_reference === result.public_reference);
          if (createdCase) {
            const formData = new FormData();
            formData.append('file', selectedFile);
            await api.post(`/cases/${createdCase.id}/evidence`, formData);
          }
        } catch (uploadErr) {
          console.warn('Evidence file upload deferred:', uploadErr);
        }
      }

      // Populate Success Modal
      document.getElementById('displayPublicRef').textContent = result.public_reference;
      document.getElementById('displayTrackingSecret').textContent = result.tracking_secret;

      if (result.urgent_guidance) {
        const uBox = document.getElementById('modalUrgentAlert');
        if (uBox) {
          uBox.style.display = 'block';
          uBox.textContent = result.urgent_guidance;
        }
      }

      openModal('credentialsModal');
    } catch (err) {
      showToast(err.message || 'Submission failed. Please check required fields.', 'error');
      submitBtn.disabled = false;
      submitBtn.textContent = 'Submit Secure Report';
    }
  });

  // Modal copy buttons
  document.getElementById('copyRefBtn')?.addEventListener('click', () => {
    const ref = document.getElementById('displayPublicRef').textContent;
    copyToClipboard(ref, 'Reference copied!');
  });

  document.getElementById('copySecretBtn')?.addEventListener('click', () => {
    const sec = document.getElementById('displayTrackingSecret').textContent;
    copyToClipboard(sec, 'Tracking Secret copied!');
  });

  document.getElementById('copyAllCredsBtn')?.addEventListener('click', () => {
    const ref = document.getElementById('displayPublicRef').textContent;
    const sec = document.getElementById('displayTrackingSecret').textContent;
    const text = `Campus Safety Report Credentials\nReference: ${ref}\nTracking Secret: ${sec}\nTrack at: ${window.location.origin}/track.html`;
    copyToClipboard(text, 'All credentials copied! Keep them secure.');
  });
});
