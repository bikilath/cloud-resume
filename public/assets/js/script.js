// First get current count
fetch('/api/GetVisitorCount')
  .then(response => response.json())
  .then(data => {
    document.getElementById('counter').textContent = data.count;
    // Then increment (no need to handle response)
    fetch('/api/GetVisitorCount', { method: 'POST' });
  })
  .catch(error => {
    console.error('Visitor counter error:', error);
    document.getElementById('counter').textContent = '0 (offline)';
  });
