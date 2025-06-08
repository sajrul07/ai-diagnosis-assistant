
const API_URL = "http://127.0.0.1:8000";

// --- Auth helpers ---
function isLoggedIn() {
  return !!localStorage.getItem('token');
}
function logout() {
  localStorage.removeItem('token');
  window.location.href = 'landing.html';
}

// --- API Calls ---
async function register(username, password) {
  try {
    const res = await fetch(`${API_URL}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    if (res.ok) {
      return { success: true, message: "Registration successful! Please login." };
    } else {
      const data = await res.json();
      return { success: false, message: data.detail || "Registration failed." };
    }
  } catch {
    return { success: false, message: "Registration failed (network error)." };
  }
}

async function login(username, password) {
  try {
    const res = await fetch(`${API_URL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    const data = await res.json();
    if (res.ok && data.token) {
      localStorage.setItem('token', data.token);
      return { success: true, message: "Login successful!" };
    } else {
      return { success: false, message: data.detail || "Login failed." };
    }
  } catch {
    return { success: false, message: "Login failed (network error)." };
  }
}

async function analyze(payload) {
  try {
    const res = await fetch(`${API_URL}/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + localStorage.getItem('token')
      },
      body: JSON.stringify(payload)
    });
    if (res.ok) {
      const data = await res.json();
      return { success: true, message: "Analysis successful!", data };
    } else {
      const data = await res.json();
      return { success: false, message: data.detail || "Analysis failed." };
    }
  } catch {
    return { success: false, message: "Analysis failed (network error)." };
  }
}