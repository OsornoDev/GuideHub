from django.urls import path
from .views import UserListView, UserDetailView, UserUpdateView, inicio_sesion
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('usuario/<int:pk>/editar/', UserUpdateView.as_view(), name='user-update'),
    path('usuario/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('usuarios/', UserListView.as_view(), name='user-list'),
    path('login/', inicio_sesion, name='login'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]