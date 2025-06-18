// Funciones para cambiar entre login y registro
        document.getElementById('switch-to-register').addEventListener('click', function(e) {
            e.preventDefault();
            document.getElementById('login-form').classList.add('d-none');
            document.getElementById('register-form').classList.remove('d-none');
            document.getElementById('login-tab').classList.remove('active');
            document.getElementById('register-tab').classList.add('active');
        });
        
        document.getElementById('switch-to-login').addEventListener('click', function(e) {
            e.preventDefault();
            document.getElementById('register-form').classList.add('d-none');
            document.getElementById('login-form').classList.remove('d-none');
            document.getElementById('register-tab').classList.remove('active');
            document.getElementById('login-tab').classList.add('active');
        });
        
        document.getElementById('register-tab').addEventListener('click', function() {
            document.getElementById('login-form').classList.add('d-none');
            document.getElementById('register-form').classList.remove('d-none');
            document.getElementById('login-tab').classList.remove('active');
            this.classList.add('active');
        });
        
        document.getElementById('login-tab').addEventListener('click', function() {
            document.getElementById('register-form').classList.add('d-none');
            document.getElementById('login-form').classList.remove('d-none');
            document.getElementById('register-tab').classList.remove('active');
            this.classList.add('active');
        });
        
        // Funcionalidad para mostrar/ocultar contraseña
        function setupPasswordToggle(inputId, toggleId) {
            const passwordInput = document.getElementById(inputId);
            const togglePassword = document.getElementById(toggleId);
            
            togglePassword.addEventListener('click', function() {
                const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
                passwordInput.setAttribute('type', type);
                this.querySelector('i').classList.toggle('bi-eye');
                this.querySelector('i').classList.toggle('bi-eye-slash');
            });
        }
        
        setupPasswordToggle('login-password', 'toggle-login-password');
        setupPasswordToggle('register-password', 'toggle-register-password');
        
        // Validación de contraseña en tiempo real
        const passwordInput = document.getElementById('register-password');
        passwordInput.addEventListener('input', validatePassword);
        
        function validatePassword() {
            const password = passwordInput.value;
            let validCount = 0;
            const totalRules = 6;
            
            // Validar longitud mínima
            const lengthValid = password.length >= 8;
            updateRule('length', lengthValid);
            if (lengthValid) validCount++;
            
            // Validar mayúscula
            const uppercaseValid = /[A-Z]/.test(password);
            updateRule('uppercase', uppercaseValid);
            if (uppercaseValid) validCount++;
            
            // Validar minúscula
            const lowercaseValid = /[a-z]/.test(password);
            updateRule('lowercase', lowercaseValid);
            if (lowercaseValid) validCount++;
            
            // Validar carácter especial
            const specialValid = /[^a-zA-Z0-9]/.test(password);
            updateRule('special', specialValid);
            if (specialValid) validCount++;
            
            // Validar números consecutivos
            const consecutiveValid = !/(012|123|234|345|456|567|678|789|890)/.test(password);
            updateRule('consecutive', consecutiveValid);
            if (consecutiveValid) validCount++;
            
            // Validar letras consecutivas
            const alphabet = 'abcdefghijklmnopqrstuvwxyz';
            const lowered = password.toLowerCase();
            let lettersValid = true;
            
            for (let i = 0; i < lowered.length - 2; i++) {
                const sub = lowered.substring(i, i + 3);
                if (alphabet.includes(sub)) {
                    lettersValid = false;
                    break;
                }
            }
            
            updateRule('letters', lettersValid);
            if (lettersValid) validCount++;
            
            // Actualizar barra de fortaleza
            const strengthBar = document.getElementById('password-strength-bar');
            const percentage = (validCount / totalRules) * 100;
            strengthBar.style.width = `${percentage}%`;
            
            // Actualizar color de la barra
            if (percentage < 40) {
                strengthBar.style.backgroundColor = '#dc3545';
            } else if (percentage < 80) {
                strengthBar.style.backgroundColor = '#ffc107';
            } else {
                strengthBar.style.backgroundColor = '#198754';
            }
        }
        
        function updateRule(ruleName, isValid) {
            const icon = document.getElementById(`${ruleName}-icon`);
            const text = document.getElementById(`${ruleName}-text`);
            
            if (isValid) {
                icon.innerHTML = '<i class="bi bi-check-circle"></i>';
                icon.classList.remove('rule-invalid');
                icon.classList.add('rule-valid');
                text.classList.remove('rule-invalid');
                text.classList.add('rule-valid');
            } else {
                icon.innerHTML = '<i class="bi bi-x-circle"></i>';
                icon.classList.remove('rule-valid');
                icon.classList.add('rule-invalid');
                text.classList.remove('rule-valid');
                text.classList.add('rule-invalid');
            }
        }
        
        // Prevenir envío de formularios para la demo
        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                alert('Formulario enviado');
            });
        });