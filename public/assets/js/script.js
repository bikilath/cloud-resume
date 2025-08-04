const API_URL = 'https://ambitious-forest-0b0181503.2.azurestaticapps.net/api/visitor/';
async function updateCounter() {
  const counterEl = document.getElementById('counter');
  try {
    counterEl.textContent = '...';
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    if (!response.ok) throw new Error('Failed to increment counter');
    const data = await response.json();
    counterEl.textContent = data.count;
    counterEl.style.color = '';
  } catch (error) {
    console.error('Counter error:', error);
    counterEl.textContent = '0 (offline)';
    counterEl.style.color = '#ff6b6b';
  }
}
window.addEventListener('DOMContentLoaded', updateCounter);
