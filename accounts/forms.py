from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
import re

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

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
    
    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if errors := validate_password(password):
            raise forms.ValidationError(errors)
        return password

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Usuario/Email")
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if '@' in username:
            try:
                return User.objects.get(email=username).username
            except User.DoesNotExist:
                pass
        return username