from django.db import models
from django.core.validators import MinValueValidator

class Disciplina(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Disciplina Deportiva")
    descripcion = models.TextField(blank=True, verbose_name="Descripción de la Disciplina")

    def __str__(self):
        return self.nombre


class Cancha(models.Model):
    ESTADOS_CHOICES = [
        ('DISPONIBLE', 'Disponible'),
        ('MANTENIMIENTO', 'En Mantenimiento'),
        ('RESERVADA', 'Reservada Completa'),
    ]

    codigo = models.CharField(max_length=10, unique=True, verbose_name="Código Único")
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la Cancha")
    disciplina = models.ForeignKey(Disciplina, on_delete=models.PROTECT, related_name="canchas", verbose_name="Disciplina")
    superficie = models.CharField(max_length=50, verbose_name="Tipo de Superficie")
    
    # Atributo cuantitativo protegido contra valores negativos
    tarifa_bloque = models.IntegerField(
        validators=[MinValueValidator(0)], 
        verbose_name="Tarifa por Bloque Horario ($)"
    )
    
    estado = models.CharField(max_length=20, choices=ESTADOS_CHOICES, default='DISPONIBLE', verbose_name="Estado Operativo")
    imagen = models.ImageField(upload_to="canchas/", blank=True, null=True, verbose_name="Imagen de la Cancha")
    activo = models.BooleanField(default=True, verbose_name="Registro Activo (Vigente)")

    def __str__(self):
        return f"{self.nombre} ({self.codigo}) - {self.disciplina.nombre}"
