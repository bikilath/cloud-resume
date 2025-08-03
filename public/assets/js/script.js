document.addEventListener('DOMContentLoaded', () => {
    fetch('/api/GetVisitorCount')
        .then(response => response.json())
        .then(data => {
            document.getElementById('counter').textContent = data.count;
            // Fire-and-forget increment
            fetch('/api/GetVisitorCount', { method: 'POST' });
        })
        .catch(error => {
            console.error('Counter error:', error);
            document.getElementById('counter').textContent = '0 (offline)';
        });
});
