const API_URL = 'https://bikila-resume-api-gyckc6b0g4fwf6gt.uksouth-01.azurewebsites.net/api/visitor';

async function updateCounter() {
  const counterEl = document.getElementById('counter');
  
  try {
    // 1. First increment the counter (POST)
    const incrementResponse = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    if (!incrementResponse.ok) throw new Error('Increment failed');

    // 2. Then get the updated count (GET)
    const getResponse = await fetch(API_URL);
    if (!getResponse.ok) throw new Error('Failed to get count');
    
    const data = await getResponse.json();
    counterEl.textContent = data.count;
    counterEl.style.color = '';
  } catch (error) {
    console.error('Counter error:', error);
    counterEl.textContent = '0 (offline)';
    counterEl.style.color = '#ff6b6b';
  }
}

window.addEventListener('DOMContentLoaded', updateCounter);
