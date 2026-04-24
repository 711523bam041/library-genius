// Authentication handlers

// Login form handler
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const loginBtn = document.getElementById('loginBtn');
        const spinner = document.getElementById('loginSpinner');
        
        // Show loading
        loginBtn.disabled = true;
        spinner.classList.remove('d-none');
        
        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            
            const data = await response.json();
            
            if (data.success) {
                showAlert('Login successful! Redirecting...', 'success');
                setTimeout(() => {
                    window.location.href = '/';
                }, 1000);
            } else {
                showAlert(data.message || 'Login failed', 'danger');
                loginBtn.disabled = false;
                spinner.classList.add('d-none');
            }
        } catch (error) {
            showAlert('An error occurred. Please try again.', 'danger');
            loginBtn.disabled = false;
            spinner.classList.add('d-none');
        }
    });
}

// Register form handler
const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm_password').value;
        const registerBtn = document.getElementById('registerBtn');
        const spinner = document.getElementById('registerSpinner');
        
        // Validate passwords match
        if (password !== confirmPassword) {
            showAlert('Passwords do not match', 'danger');
            return;
        }
        
        // Validate password length
        if (password.length < 6) {
            showAlert('Password must be at least 6 characters', 'danger');
            return;
        }
        
        // Show loading
        registerBtn.disabled = true;
        spinner.classList.remove('d-none');
        
        try {
            const response = await fetch('/api/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, email, password })
            });
            
            const data = await response.json();
            
            if (data.success) {
                showAlert('Registration successful! Redirecting to login...', 'success');
                setTimeout(() => {
                    window.location.href = '/login';
                }, 2000);
            } else {
                showAlert(data.message || 'Registration failed', 'danger');
                registerBtn.disabled = false;
                spinner.classList.add('d-none');
            }
        } catch (error) {
            showAlert('An error occurred. Please try again.', 'danger');
            registerBtn.disabled = false;
            spinner.classList.add('d-none');
        }
    });
}
