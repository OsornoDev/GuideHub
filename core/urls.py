from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('session-status/', views.session_status, name='session-status')
]
