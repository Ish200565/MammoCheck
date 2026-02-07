// Appointments Management JavaScript

/**
 * Toggle select all checkboxes
 */
function toggleSelectAll() {
    const selectAllCheckbox = document.getElementById('selectAll');
    const checkboxes = document.querySelectorAll('.appointment-checkbox');
    
    checkboxes.forEach(checkbox => {
        checkbox.checked = selectAllCheckbox.checked;
    });
    
    updateSendButton();
}

/**
 * Update the send email button state based on selected checkboxes
 */
function updateSendButton() {
    const checkboxes = document.querySelectorAll('.appointment-checkbox:checked');
    const sendButton = document.getElementById('sendEmailBtn');
    
    if (checkboxes.length > 0) {
        sendButton.disabled = false;
        sendButton.textContent = `📧 Send Email to ${checkboxes.length} Patient(s)`;
    } else {
        sendButton.disabled = true;
        sendButton.textContent = '📧 Send Confirmation Emails';
    }
    
    // Update select all checkbox state
    const allCheckboxes = document.querySelectorAll('.appointment-checkbox');
    const selectAllCheckbox = document.getElementById('selectAll');
    
    if (selectAllCheckbox) {
        selectAllCheckbox.checked = allCheckboxes.length > 0 && 
                                     checkboxes.length === allCheckboxes.length;
    }
}

/**
 * Send emails to selected appointments
 */
function sendSelectedEmails() {
    const checkboxes = document.querySelectorAll('.appointment-checkbox:checked');
    
    if (checkboxes.length === 0) {
        alert('Please select at least one appointment to send emails.');
        return;
    }
    
    const count = checkboxes.length;
    const confirmMsg = `Are you sure you want to send confirmation emails to ${count} patient(s)?`;
    
    if (confirm(confirmMsg)) {
        document.getElementById('emailForm').submit();
    }
}

/**
 * Set minimum date for appointment date picker to today
 */
document.addEventListener('DOMContentLoaded', function() {
    const dateInput = document.getElementById('appointment_date');
    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.setAttribute('min', today);
    }
    
    // Initialize button state
    updateSendButton();
});

/**
 * Auto-hide flash messages after 5 seconds
 */
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 5000);
    });
});

/**
 * Validate email format
 */
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

/**
 * Form validation before submission
 */
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.appointment-form form');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            const emailInput = document.getElementById('patient_email');
            
            if (emailInput && !validateEmail(emailInput.value)) {
                e.preventDefault();
                alert('Please enter a valid email address.');
                emailInput.focus();
                return false;
            }
        });
    }
});
