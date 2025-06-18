from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import login, authenticate
# Create your views here.


def inicio_sesion(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('inicio')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})