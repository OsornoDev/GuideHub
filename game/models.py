from django.db import models

# Create your models here.

class Plataforma(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Genero(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Videojuego(models.Model):
    rawg_id           = models.IntegerField(unique=True)
    name              = models.CharField("Título", max_length=200)
    slug              = models.SlugField(max_length=200, unique=True)
    description       = models.TextField(blank=True)
    background_image  = models.URLField("Imagen", blank=True)
    released          = models.DateField("Fecha de lanzamiento", null=True, blank=True)
    rating            = models.DecimalField("Puntuación", max_digits=3, decimal_places=2)
    metacritic        = models.IntegerField(null=True, blank=True)
    plataformas       = models.ManyToManyField(Plataforma, related_name="videojuegos", blank=True)
    generos           = models.ManyToManyField(Genero, related_name="videojuegos", blank=True)
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-rating']
        verbose_name = "Videojuego"
        verbose_name_plural = "Videojuegos"

    def __str__(self):
        return self.name