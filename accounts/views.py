from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import CustomUser
from .forms import CustomUserChangeForm, LoginForm, RegistroForm
from django.urls import reverse
from accounts.email import send_mail_django
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django import forms
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
import requests


def prueba(request):
    form = RegistroForm()
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    return render(request, 'prueba.html', {'form': form})	


class UserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-date_joined')


class UserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'accounts/user_detail.html'
    context_object_name = 'user_profile'

    def test_func(self):
        user = self.request.user
        target_user = self.get_object()
        return (
            user == target_user or
            user.is_superuser or
            (user.user_type == 'admin' and target_user.user_type != 'admin') or
            (user.user_type == 'editor' and target_user.user_type == 'user')
        )


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'user_form.html'
    
    def test_func(self):
        return self.request.user == self.get_object() or self.request.user.is_staff
    
    def get_success_url(self):
        return reverse('user-detail', kwargs={'pk': self.object.pk})

def verify_recaptcha(token: str) -> bool:
    if not token:
        return False
    resp = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data={
            "secret": settings.RECAPTCHA_PRIVATE_KEY,
            "response": token
        },
        timeout=10
    )
    try:
        result = resp.json()
    except Exception:
        return False
    return result.get("success", False)


def inicio_sesion(request):
    login_form  = LoginForm(request, data=request.POST if request.POST.get('form_type') == 'login' else None, prefix='login')
    signup_form = RegistroForm(request.POST if request.POST.get('form_type') == 'signup' else None, prefix='signup')

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        # LOGIN
        if form_type == 'login' and login_form.is_valid():
            user = login_form.get_user()
            if not user.is_active:
                return render(request, 'cuenta_no_activada.html')
            auth_login(request, user)
            return redirect('home')

        # REGISTRO
        if form_type == 'signup' and signup_form.is_valid():
            user = signup_form.save(commit=False)
            user.is_active = False  # Usuario inactivo hasta activar
            user.save()

            # Generar token y URL de activación
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activate_url = request.build_absolute_uri(
                reverse('activar_cuenta', kwargs={'uidb64': uid, 'token': token})
            )

            # Enviar correo
            send_mail_django(
                to_email=user.email,
                subject="Activa tu cuenta en GuideHub",
                template_name="bienvenida",
                data={
                    "usuario": user.username,
                    "activate_url": activate_url
                }
            )

            return render(request, 'revisar.html')  # Página que dice "Revisa tu correo"

    return render(request, 'login.html', {
        'login_form':  login_form,
        'signup_form': signup_form,
        'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY,
    })

def activar_cuenta(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'exitosa.html')
    else:
        return render(request, 'fallida.html')