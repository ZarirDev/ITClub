const PORT = "6310";
const IP = "localhost";

document.addEventListener("DOMContentLoaded", () => {
    initializePage();
});

// Initialize the page elements and event listeners
function initializePage() {
    const showPasswordCheckbox = document.getElementById("show-password");
    const usernameField = document.getElementById("username");
    const passwordField = document.getElementById("password");

    // Ensure the password checkbox is unchecked by default
    showPasswordCheckbox.checked = false;

    // Toggle password visibility
    showPasswordCheckbox.addEventListener("change", () => {
        passwordField.type = showPasswordCheckbox.checked ? "text" : "password";
    });

    // Handle Enter key in the username field
    usernameField.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            passwordField.focus();
        }
    });

    // Handle Enter key in the password field
    passwordField.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            login();
        }
    });

    // Check for an active session when the page loads
    checkSession();
}

// Display the loading screen
function showLoading() {
    const loadingScreen = document.getElementById("loading-screen");
    if (loadingScreen) {
        loadingScreen.style.display = "flex";
    }
}

// Hide the loading screen
function hideLoading() {
    const loadingScreen = document.getElementById("loading-screen");
    if (loadingScreen) {
        loadingScreen.style.display = "none";
    }
}

// Handle user login
async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const message = document.getElementById("message");

    if (!username || !password) {
        displayMessage("Please fill in all fields", "red");
        return;
    }

    showLoading();

    try {
        const response = await fetch(`http://${IP}:${PORT}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password }),
            credentials: "include",
        });

        if (!response.ok) {
            throw new Error("Failed to authenticate");
        }

        const result = await response.json();

        if (result.success) {
            await loadUserPage(result.user);
            displayMessage("Login successful!", "green");
        } else {
            displayMessage("Invalid username or password", "red");
        }
    } catch (error) {
        displayMessage("An error occurred. Please try again later", "red");
    } finally {
        hideLoading();
    }
}

// Load the user-specific page
async function loadUserPage(user) {
    showLoading();

    try {
        const response = await fetch("user_page.html");

        if (!response.ok) {
            throw new Error("Failed to load user page");
        }

        const pageContent = await response.text();
        document.body.innerHTML = pageContent;

        // Populate user data into placeholders
        document.getElementById("user-name").textContent = user.name;
        document.getElementById("user-id").textContent = user.id;
    } catch (error) {
        console.error("Error loading user page:", error);
    } finally {
        hideLoading();
    }
}

// Check if the user has an active session
async function checkSession() {
    showLoading();

    try {
        const response = await fetch(`http://${IP}:${PORT}/check_session`, {
            method: "GET",
            credentials: "include",
        });

        if (!response.ok) {
            throw new Error("Failed to check session");
        }

        const result = await response.json();

        if (result.success) {
            await loadUserPage(result.user);
        }
    } catch (error) {
        console.error("Error checking session:", error);
    } finally {
        hideLoading();
    }
}

// Log out the user and clear session data
async function logout() {
    showLoading();

    try {
        await fetch(`http://${IP}:${PORT}/logout`, {
            method: "POST",
            credentials: "include",
        });
        localStorage.removeItem("user");
        location.reload();
    } catch (error) {
        console.error("Error logging out:", error);
    } finally {
        hideLoading();
    }
}

// Display a message to the user
function displayMessage(text, color) {
    const message = document.getElementById("message");
    if (message) {
        message.style.color = color;
        message.textContent = text;
    }
}
