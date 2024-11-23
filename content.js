
// Helper function to calculate SHA-1 hash
async function sha1(password) {
  const encoder = new TextEncoder();
  const data = encoder.encode(password);
  const hashBuffer = await crypto.subtle.digest('SHA-1', data);
  return Array.from(new Uint8Array(hashBuffer))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');
}

// Function to check password breach
async function checkPasswordBreach(password) {
  const hash = await sha1(password);
  const prefix = hash.substring(0, 5);
  const suffix = hash.substring(5).toUpperCase();

  const response = await fetch(`https://api.pwnedpasswords.com/range/${prefix}`);
  if (!response.ok) {
    throw new Error('Failed to check password breach.');
  }

  const data = await response.text();
  const hashes = data.split('\n');
  for (const h of hashes) {
    const [hashSuffix, count] = h.split(':');
    if (hashSuffix === suffix) {
      return parseInt(count, 10);
    }
  }
  return 0; // No breaches found
}

// Function to display a warning near the password field
function showWarning(inputField, message, isBreached) {
  let warningElement = inputField.nextElementSibling;

  // Remove existing warning
  if (warningElement && warningElement.classList.contains('password-warning')) {
    warningElement.remove();
  }

  // Create and append new warning
  warningElement = document.createElement('div');
  warningElement.textContent = message;
  warningElement.className = 'password-warning';
  warningElement.style.color = isBreached ? 'red' : 'green';
  warningElement.style.fontSize = '12px';
  warningElement.style.marginTop = '5px';
  inputField.insertAdjacentElement('afterend', warningElement);
}

// Attach an event listener to password fields dynamically
function monitorPasswordField(field) {
  field.addEventListener('input', async (e) => {
    const password = e.target.value;

    // Skip empty passwords
    if (password.length === 0) {
      showWarning(field, '', false);
      return;
    }

    try {
      const breaches = await checkPasswordBreach(password);
      if (breaches > 0) {
        showWarning(field, `This password has been breached ${breaches} times!`, true);
      } else {
        showWarning(field, 'This password is not found in breaches.', false);
      }
    } catch (error) {
      console.error('Error checking password:', error);
    }
  });
}

// Detect password fields dynamically with mouse movement and focus
function detectPasswordFields() {
  document.addEventListener('mousemove', (e) => {
    const target = e.target;

    if (target.tagName === 'INPUT' && target.type === 'password') {
      monitorPasswordField(target);
    }
  });

  document.addEventListener('focus', (e) => {
    const target = e.target;

    if (target.tagName === 'INPUT' && target.type === 'password') {
      monitorPasswordField(target);
    }
  }, true);
}

// Initialize detection
detectPasswordFields();
