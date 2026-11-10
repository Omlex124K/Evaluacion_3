from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from canchas.models import Disciplina, Cancha

class Command(BaseCommand):
    help = 'Pobla la base de datos con datos de prueba obligatorios para la evaluación'

    def handle(self, *args, **kwargs):
        # 1. Crear Usuarios de prueba obligatorios
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@matchpoint.cl', 'admin123')
        if not User.objects.filter(username='operador').exists():
            User.objects.create_user('operador', 'operador@matchpoint.cl', 'user123')

        # 2. Crear 4 Disciplinas (Contextos exigidos)
        padel, _ = Disciplina.objects.get_or_create(nombre="Pádel", descripcion="Canchas de cristal con iluminación LED")
        tenis, _ = Disciplina.objects.get_or_create(nombre="Tenis", descripcion="Canchas de arcilla profesionales")
        futbol, _ = Disciplina.objects.get_or_create(nombre="Fútbol", descripcion="Canchas de pasto sintético con drenaje")
        basket, _ = Disciplina.objects.get_or_create(nombre="Básquetbol", descripcion="Gimnasio techado con piso de parquet")

        # 3. Crear 8 Canchas (Entidades Principales coherentes)
        canchas_datos = [
            {"codigo": "PD-01", "nombre": "Cancha Pádel Central", "disciplina": padel, "superficie": "Cristal Panorámico", "tarifa_bloque": 18000},
            {"codigo": "PD-02", "nombre": "Cancha Pádel Express", "disciplina": padel, "superficie": "Cristal Estándar", "tarifa_bloque": 15000},
            {"codigo": "TN-01", "nombre": "Court Central Nadal", "disciplina": tenis, "superficie": "Arcilla", "tarifa_bloque": 12000},
            {"codigo": "TN-02", "nombre": "Cancha Tenis Rápida", "disciplina": tenis, "superficie": "Asfalto Cemento", "tarifa_bloque": 10000},
            {"codigo": "FB-01", "nombre": "Estadio Fútbol 7", "disciplina": futbol, "superficie": "Pasto Sintético", "tarifa_bloque": 25000},
            {"codigo": "FB-02", "nombre": "Cancha Fútbol 5 Kids", "disciplina": futbol, "superficie": "Pasto Sintético", "tarifa_bloque": 20000},
            {"codigo": "BK-01", "nombre": "Gimnasio Principal", "disciplina": basket, "superficie": "Parquet", "tarifa_bloque": 30000},
            {"codigo": "BK-02", "nombre": "Multicancha Exterior", "disciplina": basket, "superficie": "Cemento Pintado", "tarifa_bloque": 12000},
        ]

        for datos in canchas_datos:
            Cancha.objects.get_or_create(codigo=datos["codigo"], defaults=datos)

        self.stdout.write(self.style.SUCCESS('Base de datos poblada exitosamente con 4 disciplinas, 8 canchas y usuarios.'))
