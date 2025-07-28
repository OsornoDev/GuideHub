from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
# Create your models here.


class CustomUser(AbstractUser):
    USER_TYPES = (
        ('admin', 'Administrador'),
        ('user', 'Usuario Regular'),
    )
    
    user_type = models.CharField(
        max_length=20, 
        choices=USER_TYPES, 
        default='user',
        verbose_name=_('Tipo de Usuario')
    )
    bio = models.TextField(
        blank=True, 
        null=True,
        verbose_name=_('Biografía')
    )
    avatar = models.ImageField(
        upload_to='avatars/', 
        blank=True, 
        null=True,
        verbose_name=_('Avatar')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Fecha de Creación')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Última Actualización')
    )
    
    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')
        ordering = ['-date_joined']