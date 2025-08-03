// Visitor counter with proper incrementing
async function updateCounter() {
  const counterElement = document.getElementById('counter');
  
  try {
    // First increment the counter (POST)
    const incrementResponse = await fetch('/api/GetVisitorCount', {
      method: 'POST'
    });
    
    if (!incrementResponse.ok) {
      throw new Error('Failed to increment counter');
    }
    
    // Then get the updated count (GET)
    const getResponse = await fetch('/api/GetVisitorCount');
    const data = await getResponse.json();
    
    counterElement.textContent = data.count;
    counterElement.style.color = ''; // Reset error color if any
    
  } catch (error) {
    console.error('Counter error:', error);
    counterElement.textContent = '0 (offline)';
    counterElement.style.color = '#ff6b6b';
  }
}

// Initialize when page loads
window.addEventListener('DOMContentLoaded', updateCounter);
