// ==================== STATE MANAGEMENT ====================
const STATE = {
    currentRole: null,
    selectedRole: null,
    patients: JSON.parse(localStorage.getItem('patients')) || [],
    currentPatientIndex: null
};

// ==================== ROLE SELECTION ====================
function setRoleSelection(role) {
    STATE.selectedRole = role;
    
    // Update UI to show selection
    document.querySelectorAll('.role-card').forEach(card => {
        card.classList.remove('selected');
    });
    
    const selectedCard = document.querySelector(`.${role}-card`);
    if (selectedCard) {
        selectedCard.classList.add('selected');
    }
    
    // Enable Google login button
    const googleBtn = document.getElementById('googleLoginBtn');
    if (googleBtn) {
        googleBtn.disabled = false;
        googleBtn.classList.add('enabled');
    }
    
    // Update login note
    const loginNote = document.querySelector('.login-note');
    if (loginNote) {
        loginNote.textContent = `Continue as ${role.charAt(0).toUpperCase() + role.slice(1)} with Google`;
        loginNote.style.color = '#4285F4';
    }
}

function loginWithGoogle() {
    if (!STATE.selectedRole) {
        alert('Please select your role (Doctor or Radiologist) before signing in');
        return;
    }
    
    // Redirect to Google OAuth login with selected role
    window.location.href = `/login/google/${STATE.selectedRole}`;
}

// ==================== PAGE NAVIGATION ====================
function selectRole(role) {
    STATE.currentRole = role;
    
    // Send login request to server to establish session (backward compatibility)
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ role: role })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = data.redirect;
        } else {
            alert('Login failed: ' + (data.error || 'Unknown error'));
        }
    })
    .catch(error => {
        console.error('Login error:', error);
        alert('Failed to log in. Please try again.');
    });
}

function logout() {
    STATE.currentRole = null;
    STATE.currentPatientIndex = null;
    window.location.href = '/logout';
}

// ==================== RADIOLOGIST FUNCTIONS ====================
function addPatient(event) {
    event.preventDefault();
    const name = document.getElementById('patientName').value.trim();
    const age = document.getElementById('patientAge').value;
    const phone = document.getElementById('patientPhone').value.trim();
    const patientID = document.getElementById('patientID').value.trim();
    const notes = document.getElementById('patientNotes').value.trim();
    
    if (!name || !age || !phone || !patientID) {
        alert('Please fill in all required patient details');
        return;
    }
    
    const images = ['LCC', 'LMLO', 'RCC', 'RMLO'];
    const selectedFiles = {};
    for (let view of images) {
        const input = document.getElementById(view);
        if (!input.files || !input.files[0]) {
            alert(`Please upload ${view} image`);
            return;
        }
        selectedFiles[view] = input.files[0];
    }
    
    showLoadingSpinner(true);
    
    const formData = new FormData();
    for (let view of images) {
        formData.append(view, selectedFiles[view]);
    }
    
    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        const classifications = {};
        const errors = [];
        
        data.results.forEach(item => {
            if (item.error) {
                errors.push(`${item.view}: ${item.error}`);
            } else {
                classifications[item.view] = {
                    label: item.label,
                    confidence: item.confidence,
                    prediction: item.prediction,
                    time: item.time
                };
            }
        });
        
        if (errors.length > 0) {
            alert('Errors during classification:\n' + errors.join('\n'));
            showLoadingSpinner(false);
            return;
        }
        
        const patient = {
            patientID,
            name,
            age: parseInt(age),
            phone,
            notes,
            addedDate: new Date().toLocaleString(),
            imageBase64: {},
            classifications
        };
        
        const imagePromises = images.map(view => {
            return new Promise((resolve) => {
                const reader = new FileReader();
                reader.onload = (e) => {
                    patient.imageBase64[view] = e.target.result;
                    resolve();
                };
                reader.readAsDataURL(selectedFiles[view]);
            });
        });
        
        Promise.all(imagePromises).then(() => {
            STATE.patients.push(patient);
            localStorage.setItem('patients', JSON.stringify(STATE.patients));
            document.getElementById('patientForm').reset();
            populateRadiologistDashboard();
            showLoadingSpinner(false);
            alert('Patient added successfully! Images have been classified.');
        });
    })
    .catch(err => {
        showLoadingSpinner(false);
        alert('Error classifying images: ' + err.message);
    });
}

function populateRadiologistDashboard() {
    const listDiv = document.getElementById('radiologistPatientsList');
    if (!listDiv) return;
    
    if (STATE.patients.length === 0) {
        listDiv.innerHTML = '<p class="no-data-msg">No patients added yet.</p>';
        return;
    }
    
    listDiv.innerHTML = STATE.patients.map((patient, idx) => `
        <div class="patient-card">
            <div class="patient-card-header">
                <h4>${patient.name}</h4>
                <span class="patient-id">ID: ${patient.patientID}</span>
            </div>
            <div class="patient-card-body">
                <p><strong>Age:</strong> ${patient.age}</p>
                <p><strong>Phone:</strong> ${patient.phone}</p>
                <p><strong>Added:</strong> ${patient.addedDate}</p>
                ${patient.notes ? `<p><strong>Notes:</strong> ${patient.notes}</p>` : ''}
            </div>
            <div class="patient-classification-summary">
                <strong>Classifications:</strong>
                <ul>
                    ${Object.entries(patient.classifications).map(([view, clf]) => 
                        `<li>${view}: ${clf.label} (${clf.confidence})</li>`
                    ).join('')}
                </ul>
            </div>
            <button class="delete-btn" onclick="deletePatient(${idx})">Delete</button>
        </div>
    `).join('');
}

function deletePatient(index) {
    if (confirm('Are you sure you want to delete this patient record?')) {
        STATE.patients.splice(index, 1);
        localStorage.setItem('patients', JSON.stringify(STATE.patients));
        populateRadiologistDashboard();
    }
}

// ==================== DOCTOR FUNCTIONS ====================
function populateDoctorDashboard() {
    const listDiv = document.getElementById('patientsList');
    const noDataDiv = document.getElementById('noPatientsMsg');
    if (!listDiv || !noDataDiv) return;
    
    if (STATE.patients.length === 0) {
        listDiv.innerHTML = '';
        noDataDiv.style.display = 'block';
        return;
    }
    
    noDataDiv.style.display = 'none';
    listDiv.innerHTML = STATE.patients.map((patient, idx) => `
        <div class="patient-card doctor-card" onclick="viewPatientDetails(${idx})">
            <h4>${patient.name}</h4>
            <p><strong>ID:</strong> ${patient.patientID}</p>
            <p><strong>Age:</strong> ${patient.age}</p>
            <p><strong>Phone:</strong> ${patient.phone}</p>
            <p class="card-added">${patient.addedDate}</p>
            <button class="view-btn">View Full Details</button>
        </div>
    `).join('');
}

function filterPatients() {
    const searchInput = document.getElementById('doctorSearchInput');
    if (!searchInput) return;
    
    const searchValue = searchInput.value.toLowerCase();
    const cards = document.querySelectorAll('#patientsList .patient-card');
    
    cards.forEach(card => {
        const text = card.textContent.toLowerCase();
        card.style.display = text.includes(searchValue) ? 'block' : 'none';
    });
}

function viewPatientDetails(index) {
    STATE.currentPatientIndex = index;
    const patient = STATE.patients[index];
    const modal = document.getElementById('patientModal');
    if (!modal) return;
    
    const detailsDiv = document.getElementById('patientDetails');
    if (detailsDiv) {
        detailsDiv.innerHTML = `
            <div class="detail-row">
                <span class="detail-label">Name:</span>
                <span class="detail-value">${patient.name}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Patient ID:</span>
                <span class="detail-value">${patient.patientID}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Age:</span>
                <span class="detail-value">${patient.age} years</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Contact:</span>
                <span class="detail-value">${patient.phone}</span>
            </div>
            ${patient.notes ? `
            <div class="detail-row">
                <span class="detail-label">Clinical Notes:</span>
                <span class="detail-value">${patient.notes}</span>
            </div>
            ` : ''}
            <div class="detail-row">
                <span class="detail-label">Date Added:</span>
                <span class="detail-value">${patient.addedDate}</span>
            </div>
        `;
    }
    
    const imagesDiv = document.getElementById('patientImages');
    if (imagesDiv) {
        imagesDiv.innerHTML = '<h3>Classified Mammogram Images</h3><div class="images-grid">' +
            Object.entries(patient.classifications).map(([view, clf]) => `
                <div class="image-card">
                    <img src="${patient.imageBase64[view]}" alt="${view}">
                    <div class="classification-info">
                        <h5>${view}</h5>
                        <p class="classification-label">${clf.label}</p>
                        <p class="classification-confidence">Confidence: ${clf.confidence}</p>
                    </div>
                </div>
            `).join('') +
            '</div>';
    }
    
    modal.style.display = 'block';
}

function closePatientModal() {
    const modal = document.getElementById('patientModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

function showLoadingSpinner(show) {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) {
        spinner.style.display = show ? 'flex' : 'none';
    }
}

// ==================== UTILITIES ====================
window.onclick = function(event) {
    const modal = document.getElementById('patientModal');
    if (modal && event.target === modal) {
        modal.style.display = 'none';
    }
};

// ==================== INITIALIZE ====================
document.addEventListener('DOMContentLoaded', function() {
    // Initialize radiologist dashboard if on that page
    if (document.getElementById('radiologistPatientsList')) {
        populateRadiologistDashboard();
    }
    
    // Initialize doctor dashboard if on that page
    if (document.getElementById('patientsList')) {
        populateDoctorDashboard();
    }
});
