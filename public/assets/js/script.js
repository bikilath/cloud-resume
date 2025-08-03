document.addEventListener('DOMContentLoaded', () => {
    const counterElement = document.getElementById('counter');
    
    // First try to get the current count
    fetch('/api/GetVisitorCount')
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            counterElement.textContent = data.count;
            
            // Then increment the count (fire and forget)
            fetch('/api/GetVisitorCount', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            }).catch(error => console.error('Increment failed:', error));
        })
        .catch(error => {
            console.error('Visitor counter error:', error);
            counterElement.textContent = '0 (offline)';
        });
    
    // Update copyright year
    document.getElementById('year').textContent = new Date().getFullYear();
});
