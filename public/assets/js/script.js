// Update counter (call this on page load)
async function getCount() {
  const response = await fetch('/api/GetVisitorCount');
  const data = await response.json();
  document.getElementById('counter').textContent = data.count;
}

// Increment counter (call this when needed)
async function incrementCount() {
  await fetch('/api/GetVisitorCount', { method: 'POST' });
  await getCount(); // Refresh display
}

// Initialize
window.addEventListener('DOMContentLoaded', getCount);
