from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import CustomUser
from .forms import CustomUserChangeForm, LoginForm, RegistroForm
from django.urls import reverse
# Create your views here.

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
                # Filtros adicionales si es necesario
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
        
def inicio_sesion(request):
    login_form    = LoginForm(request, data=request.POST or None, prefix='login')
    signup_form   = RegistroForm(request.POST or None, prefix='signup')

    # solo procesamos si es POST
    if request.method == 'POST':
        # sabemos qué form vino por este campo oculto
        form_type = request.POST.get('form_type')

        if form_type == 'login' and login_form.is_valid():
            print('login')
            user = login_form.get_user()
            print(user)
            auth_login(request, user)
            return redirect('home')

        if form_type == 'signup':
            if signup_form.is_valid():
                user = signup_form.save()
                auth_login(request, user)
                return redirect('home')
            else:
                print("Errores de registro:", signup_form.errors)

    return render(request, 'login.html', {
        'login_form':  login_form,
        'signup_form': signup_form,
    })