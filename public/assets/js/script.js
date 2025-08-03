// Set current year in footer
document.getElementById('year').textContent = new Date().getFullYear();

// Visitor counter functionality
document.addEventListener('DOMContentLoaded', function() {
    const counterElement = document.getElementById('counter');
    // Change API endpoint to:
const apiUrl = '/api/GetVisitorCount';  // Static Web Apps auto-routes /api';
    
    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        counterElement.textContent = data.count;
    })
    .catch(error => {
        console.error('Error fetching visitor count:', error);
        counterElement.textContent = '0 (offline)';
    });
});