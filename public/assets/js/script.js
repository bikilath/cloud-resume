const API_URL = 'https://bikila-resume-api-gyckc6b0g4fwf6gt.uksouth-01.azurewebsites.net/api/visitor';

async function updateCounter() {
  const counterEl = document.getElementById('counter');
  
  try {
    // First get current count
    const getResponse = await fetch(API_URL);
    if (!getResponse.ok) throw new Error(await getResponse.text());
    
    // Then increment (POST)
    const postResponse = await fetch(API_URL, { 
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    // Update display
    const data = await getResponse.json();
    counterEl.textContent = data.count;
    counterEl.style.color = ''; // Reset error style
  } catch (error) {
    console.error('Counter error:', error);
    counterEl.textContent = '0 (offline)';
    counterEl.style.color = '#ff6b6b';
  }
}

window.addEventListener('DOMContentLoaded', updateCounter);
