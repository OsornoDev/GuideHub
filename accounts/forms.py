from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import CustomUser
import re
import requests
from django.conf import settings
from django.contrib.auth import get_user_model

def validate_password(password):
    errors = []
    if len(password) < 8:
        errors.append("La contraseña debe tener al menos 8 caracteres.")
    if not re.search(r'[A-Z]', password):
        errors.append("La contraseña debe contener al menos una letra mayúscula.")
    if not re.search(r'[a-z]', password):
        errors.append("La contraseña debe contener al menos una letra minúscula.")
    if not re.search(r'[^a-zA-Z0-9]', password):
        errors.append("La contraseña debe contener al menos un carácter especial.")
    if re.search(r'(?:012|123|234|345|456|567|678|789|890)', password):
        errors.append("No se permiten números consecutivos en la contraseña.")
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    lowered = password.lower()
    for i in range(len(lowered) - 2):
        if lowered[i:i+3] in alphabet:
            errors.append("No se permiten letras consecutivas en la contraseña.")
            break
    return errors

User = get_user_model()

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuario/Email",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Usuario o email'
        })
    )
    
    password = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'password',
            'placeholder': 'Tu contraseña'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        token = self.data.get("g-recaptcha-response")

        if not token:
            raise forms.ValidationError("Por favor, completa el reCAPTCHA.")

        resp = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={
                "secret": settings.RECAPTCHA_PRIVATE_KEY,
                "response": token
            }
        )
        result = resp.json()
        if not result.get("success"):
            raise forms.ValidationError("Error en reCAPTCHA, intente de nuevo.")

        return cleaned_data
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        # Si el usuario ingresa un email, buscar el username asociado
        if username and '@' in username:
            try:
                user = User.objects.get(email=username)
                self.cleaned_data['username'] = user.username
            except User.DoesNotExist:
                # Mantener el valor original para mostrar el error estándar
                pass

        return super().clean()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_type')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_type', 'bio', 'avatar')


from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegistroForm(UserCreationForm):
    username = forms.CharField(
        label="Nombre de usuario",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'register-username',
            'placeholder': 'Tu nombre de usuario'
        })
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': 'register-email',
            'placeholder': 'tu@email.com'
        })
    )
    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'register-password',
            'placeholder': 'Crea una contraseña segura'
        })
    )
    password2 = forms.CharField(
                label="Confirmar Contraseña",
                strip=False,
                widget=forms.PasswordInput(attrs={
                    'class': 'form-control',
                    'id': 'register-password-confirm',  # antes era register-password2
                    'placeholder': 'Confirma tu contraseña'
            })
        )
    
    def clean(self):
        cleaned_data = super().clean()
        token = self.data.get("g-recaptcha-response")

        if not token:
            raise forms.ValidationError("Por favor, completa el reCAPTCHA.")

        resp = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={
                "secret": settings.RECAPTCHA_PRIVATE_KEY,
                "response": token
            }
        )
        result = resp.json()
        if not result.get("success"):
            raise forms.ValidationError("Error en reCAPTCHA, intente de nuevo.")

        return cleaned_data
    
    terms = forms.BooleanField(
            label='Acepto',
            widget=forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'terms',   # antes era register-terms
            })
        )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return email

    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        # Actualizamos widget de username
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'id': 'register-username',
            'placeholder': 'Tu nombre de usuario'
        })
        # Ajustamos widget de email
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'id': 'register-email',
            'placeholder': 'tu@email.com'
        })
        # Ocultamos help_texts por defecto si quieres
        for field in ['username', 'password1', 'password2']:
            if field in self.fields:
                self.fields[field].help_text = None

    def clean(self):
        cleaned = super().clean()
        token = self.data.get("g-recaptcha-response")
        if not token:
            raise forms.ValidationError("Por favor, completa el reCAPTCHA.")
        try:
            resp = requests.post(
                "https://www.google.com/recaptcha/api/siteverify",
                data={"secret": settings.RECAPTCHA_PRIVATE_KEY, "response": token},
                timeout=10
            )
            result = resp.json()
        except Exception:
            raise forms.ValidationError("Error validando reCAPTCHA, inténtalo de nuevo.")

        if not result.get("success"):
            raise forms.ValidationError("Error en reCAPTCHA, inténtalo de nuevo.")
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error('password2', "Las contraseñas no coinciden.")
        return cleaned
    
from django import forms

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Introduce tu correo registrado'
        })
    )
