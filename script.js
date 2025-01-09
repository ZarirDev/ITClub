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
        const response = await fetch('http://localhost:5000/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();
        if (result.success) {
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