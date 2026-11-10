from django.urls import path
from . import views

urlpatterns = [
    # Catálogo Público y Filtros
    path('', views.catalogo_publico, name='catalogo_publico'),
    
    # Módulo de Sesiones (Planificador)
    path('jornada/', views.ver_jornada, name='ver_jornada'),
    path('jornada/agregar/<int:cancha_id>/', views.agregar_a_jornada, name='agregar_a_jornada'),
    path('jornada/limpiar/', views.limpiar_jornada, name='limpiar_jornada'),
    path('jornada/confirmar/', views.confirmar_jornada, name='confirmar_jornada'),
    
    # Módulo 3: Operaciones CRUD Frontend (Backoffice Protegido)
    path('gestion/canchas/', views.gestion_canchas, name='gestion_canchas'),
    path('gestion/canchas/crear/', views.crear_cancha, name='crear_cancha'),
    path('gestion/canchas/editar/<int:pk>/', views.editar_cancha, name='editar_cancha'),
    path('gestion/canchas/eliminar/<int:pk>/', views.eliminar_cancha, name='eliminar_cancha'),
    
    # Autenticación requerida por Módulo 4
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
]
