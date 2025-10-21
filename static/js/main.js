// Toggle sidebar on mobile
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        sidebar.classList.toggle('active');
    }
}

// Modal functions
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
    }
}

// Close modal when clicking outside
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal-overlay')) {
        e.target.classList.remove('active');
    }
});

// Handle announcement posting with AJAX
function postAnnouncement(classId) {
    const form = document.getElementById('announcement-form');
    const formData = new FormData(form);
    
    fetch(`/class/${classId}/post-announcement`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('Announcement posted successfully!', 'success');
            closeModal('announcement-modal');
            form.reset();
            // Reload page to show new announcement
            setTimeout(() => location.reload(), 1000);
        } else {
            showAlert(data.message || 'Error posting announcement', 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('An error occurred', 'danger');
    });
    
    return false; // Prevent default form submission
}

// Show alert messages
function showAlert(message, type = 'info') {
    const container = document.querySelector('.flash-container') || createFlashContainer();
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.innerHTML = `
        ${message}
        <button onclick="this.parentElement.remove()">×</button>
    `;
    
    container.appendChild(alert);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        alert.remove();
    }, 5000);
}

function createFlashContainer() {
    const container = document.createElement('div');
    container.className = 'flash-container';
    document.body.appendChild(container);
    return container;
}

// Tab switching
function switchTab(tabName) {
    // Hide all tab contents
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.style.display = 'none';
    });
    
    // Remove active class from all tab links
    document.querySelectorAll('.tab-nav a').forEach(link => {
        link.classList.remove('active');
    });
    
    // Show selected tab
    const selectedTab = document.getElementById(tabName + '-tab');
    if (selectedTab) {
        selectedTab.style.display = 'block';
    }
    
    // Add active class to clicked tab link
    event.target.classList.add('active');
}

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            field.style.borderColor = '#ef4444';
            
            // Remove error styling on input
            field.addEventListener('input', function() {
                this.style.borderColor = '';
            }, { once: true });
        }
    });
    
    if (!isValid) {
        showAlert('Please fill in all required fields', 'danger');
    }
    
    return isValid;
}

// File upload preview
function handleFileSelect(inputId, previewId) {
    const input = document.getElementById(inputId);
    const preview = document.getElementById(previewId);
    
    if (!input || !preview) return;
    
    const file = input.files[0];
    if (file) {
        preview.innerHTML = `
            <div class="file-preview">
                <span>📎 ${file.name}</span>
                <span>${(file.size / 1024).toFixed(2)} KB</span>
            </div>
        `;
    }
}

// Confirm actions
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Search functionality
function searchClasses(searchTerm) {
    const cards = document.querySelectorAll('.class-card');
    const term = searchTerm.toLowerCase();
    
    cards.forEach(card => {
        const title = card.querySelector('h3').textContent.toLowerCase();
        const section = card.querySelector('p').textContent.toLowerCase();
        
        if (title.includes(term) || section.includes(term)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// Initialize search if search input exists
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.querySelector('.search-input');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            searchClasses(e.target.value);
        });
    }
    
    // Auto-hide flash messages after 5 seconds
    setTimeout(() => {
        document.querySelectorAll('.alert').forEach(alert => {
            alert.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => alert.remove(), 300);
        });
    }, 5000);
});

// Add slideOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Escape key closes modals
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal-overlay.active').forEach(modal => {
            modal.classList.remove('active');
        });
    }
});

// Copy class code to clipboard
function copyClassCode(code) {
    navigator.clipboard.writeText(code).then(() => {
        showAlert(`Class code "${code}" copied to clipboard!`, 'success');
    }).catch(() => {
        showAlert('Failed to copy class code', 'danger');
    });
}

// Format dates
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now - date;
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    
    if (days === 0) return 'Today';
    if (days === 1) return 'Yesterday';
    if (days < 7) return `${days} days ago`;
    
    return date.toLocaleDateString();
}

// Apply date formatting on page load
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-date]').forEach(element => {
        const date = element.getAttribute('data-date');
        element.textContent = formatDate(date);
    });
});