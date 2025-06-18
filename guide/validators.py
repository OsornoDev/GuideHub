import re

def validate_password(password):
    errors = []
    if len(password) < 8:
        errors.append("La contraseña debe tener al menos 8 caracteres.")
    if not re.search(r'[A-Z]', password):
        errors.append("Debe contener al menos una letra mayúscula.")
    if not re.search(r'[a-z]', password):
        errors.append("Debe contener al menos una letra minúscula.")
    if not re.search(r'[^a-zA-Z0-9]', password):
        errors.append("Debe contener al menos un carácter especial.")
    if re.search(r'(?:012|123|234|345|456|567|678|789|890)', password):
        errors.append("No se permiten números consecutivos.")
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    lowered = password.lower()
    for i in range(len(lowered) - 2):
        if lowered[i:i+3] in alphabet:
            errors.append("No se permiten letras consecutivas.")
            break
    return errors