const PORT = "5000"

document.addEventListener("DOMContentLoaded", function() {
    // Get the checkbox element and set its checked property to false
    document.getElementById('show-password').checked = false;
});

document.getElementById('show-password').addEventListener('change', function () {
    const passwordField = document.getElementById('password');
    passwordField.type = this.checked ? 'text' : 'password';
});

document.getElementById('username').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        document.getElementById('password').focus(); // Move focus to password field
    }
});

document.getElementById('password').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        login(); // Trigger login function
    }
});

async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const message = document.getElementById('message');

    if (!username || !password) {
        message.style.color = 'red';
        message.textContent = 'Please fill in all fields';
        return;
    }
    
    try {
        const response = await fetch(`http://localhost:${PORT}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
            credentials: 'include'  // Include session cookies
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();
        if (result.success) {
            await loadUserPage(result.user);
            message.style.color = 'green';
            message.textContent = 'Login successful!';
            console.log(result.success);
            console.log("Successfully logged in");
        } else {
            message.style.color = 'red';
            message.textContent = 'Invalid username or password';
            console.log(result.success);
            console.log("Invalid credentials");
        }
    } catch (error) {
        message.style.color = 'red';
        message.textContent = 'An error occurred. Please try again later';
    }
}

async function loadUserPage(user) {
    try {
        const response = await fetch('user_page.html');  // Load external HTML file
        if (!response.ok) {
            throw new Error('Failed to load user page');
        }

        const pageContent = await response.text();
        document.body.innerHTML = pageContent;  // Inject the content into body

        // Insert user-specific data into placeholders
        document.getElementById('user-name').textContent = user.name;
        document.getElementById('user-id').textContent = user.id;
    } catch (error) {
        console.error('Error loading user page:', error);
    }
}

async function checkSession() {
    try {
        const response = await fetch(`http://localhost:${PORT}/check_session`, {
            method: 'GET',
            credentials: 'include'  // Include session cookies
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();
        if (result.success) {
            await loadUserPage(result.user);  // Load user page if session exists
        }
    } catch (error) {
        console.error('Error checking session:', error);
    }
}

async function logout() {
    await fetch(`http://localhost:${PORT}/logout`, {
        method: 'POST',
        credentials: 'include'
    });
    localStorage.removeItem('user');
    location.reload();
}

// Check session on page load
window.onload = checkSession;