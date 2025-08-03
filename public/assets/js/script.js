async function updateCounter() {
  try {
    // Get current count
    const response = await fetch('/api/GetVisitorCount');
    const data = await response.json();
    document.getElementById('counter').textContent = data.count;
    
    // Increment count (fire-and-forget)
    fetch('/api/GetVisitorCount', { method: 'POST' });
  } catch (error) {
    console.error("Counter error:", error);
    document.getElementById('counter').textContent = "0 (offline)";
  }
}
document.addEventListener('DOMContentLoaded', updateCounter);
