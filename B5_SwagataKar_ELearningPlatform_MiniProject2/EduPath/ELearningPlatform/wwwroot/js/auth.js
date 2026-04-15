
function checkAuth() {
  const userId = localStorage.getItem('userId');
  const currentPage = window.location.pathname;

 
  if (currentPage.includes('login.html') ||
      currentPage.includes('register.html')) {
    return;
  }

  if (!userId) {
    window.location.href = 'login.html';
  }
}

async function login() {
  const email = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value.trim();
  const errorDiv = document.getElementById('loginError');

  if (!email || !password) {
    errorDiv.textContent = 'Please fill in all fields.';
    errorDiv.style.display = 'block';
    return;
  }

  try {
    const response = await fetch('/api/users/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    if (response.status === 401) {
      errorDiv.textContent = 'Invalid email or password.';
      errorDiv.style.display = 'block';
      return;
    }

    const user = await response.json();


    localStorage.setItem('userId', user.userId);
    localStorage.setItem('userFullName', user.fullName);
    localStorage.setItem('userEmail', user.email);


    window.location.href = 'dashboard.html';

  } catch (err) {
    errorDiv.textContent = 'Something went wrong. Try again.';
    errorDiv.style.display = 'block';
    console.error(err);
  }
}


async function register() {
  const fullName = document.getElementById('fullName').value.trim();
  const email = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value.trim();
  const errorDiv = document.getElementById('registerError');
  const successDiv = document.getElementById('registerSuccess');

  errorDiv.style.display = 'none';
  successDiv.style.display = 'none';

  if (!fullName || !email || !password) {
    errorDiv.textContent = 'Please fill in all fields.';
    errorDiv.style.display = 'block';
    return;
  }

  if (password.length < 6) {
    errorDiv.textContent = 'Password must be at least 6 characters.';
    errorDiv.style.display = 'block';
    return;
  }

  try {
    const response = await fetch('/api/users/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ fullName, email, password })
    });

    if (response.status === 400) {
      const data = await response.json();
      errorDiv.textContent = data.message || 'Registration failed.';
      errorDiv.style.display = 'block';
      return;
    }

    successDiv.textContent = 'Registered successfully! Redirecting to login...';
    successDiv.style.display = 'block';

    setTimeout(() => {
      window.location.href = 'login.html';
    }, 1500);

  } catch (err) {
    errorDiv.textContent = 'Something went wrong. Try again.';
    errorDiv.style.display = 'block';
    console.error(err);
  }
}


function logout() {
  localStorage.removeItem('userId');
  localStorage.removeItem('userFullName');
  localStorage.removeItem('userEmail');
  window.location.href = 'login.html';
}