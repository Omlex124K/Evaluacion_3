from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Cancha, Disciplina
from .forms import CanchaForm

# --- CATÁLOGO PÚBLICO y SESIONES ---

def catalogo_publico(request):
    disciplinas = Disciplina.objects.all()
    canchas = Cancha.objects.filter(activo=True).select_related('disciplina')
    disciplina_id = request.GET.get('disciplina')
    if d_id := disciplina_id:
        canchas = canchas.filter(disciplina_id=d_id)
        
    return render(request, 'canchas/catalogo.html', {
        'canchas': canchas,
        'disciplinas': disciplinas,
        'disciplina_seleccionada': int(disciplina_id) if d_id else None
    })

def agregar_a_jornada(request, cancha_id):
    if request.method == "POST":
        cancha = get_object_or_404(Cancha, id=cancha_id)
        if 'jornada' not in request.session:
            request.session['jornada'] = {}
        jornada = request.session['jornada']
        
        bloque = request.POST.get('bloque', '09:00 - 10:30')
        incluye_implementos = request.POST.get('implementos') == 'on'
        costo_implementos = 5000 if incluye_implementos else 0
        
        jornada[str(cancha.id)] = {
            'nombre': cancha.nombre,
            'codigo': cancha.codigo,
            'tarifa': cancha.tarifa_bloque,
            'bloque': bloque,
            'implementos': costo_implementos,
            'subtotal': cancha.tarifa_bloque + costo_implementos
        }
        request.session['jornada'] = jornada
    return redirect('ver_jornada')

def ver_jornada(request):
    jornada = request.session.get('jornada', {})
    total_neto = sum(item['subtotal'] for item in jornada.values())
    iva = int(total_neto * 0.19)
    return render(request, 'canchas/jornada.html', {
        'jornada': jornada,
        'total_neto': total_neto,
        'iva': iva,
        'total_general': total_neto + iva
    })

def limpiar_jornada(request):
    if 'jornada' in request.session:
        del request.session['jornada']
    return redirect('catalogo_publico')

def confirmar_jornada(request):
    # Resumen de solicitud: Vacía la sesión y simula un comprobante final según Módulo 4
    if 'jornada' in request.session:
        del request.session['jornada']
    messages.success(request, "Itinerario temporal confirmado. Solicitud enviada al sistema de agendamiento.")
    return redirect('catalogo_publico')


# --- MÓDULO 3: OPERACIONES CRUD frontend (PROTEGIDO) ---

def es_staff(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(es_staff)
def gestion_canchas(request):
    canchas = Cancha.objects.all().select_related('disciplina')
    return render(request, 'canchas/gestion_listado.html', {'canchas': canchas})

@login_required
@user_passes_test(es_staff)
def crear_cancha(request):
    if request.method == 'POST':
        form = CanchaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Cancha deportiva registrada exitosamente.")
            return redirect('gestion_canchas')
    else:
        form = CanchaForm()
    return render(request, 'canchas/form_cancha.html', {'form': form, 'titulo': 'Registrar Nueva Cancha'})

@login_required
@user_passes_test(es_staff)
def editar_cancha(request, pk):
    cancha = get_object_or_404(Cancha, pk=pk)
    if request.method == 'POST':
        form = CanchaForm(request.POST, request.FILES, instance=cancha)
        if form.is_valid():
            form.save()
            messages.success(request, "Los datos de la cancha han sido actualizados.")
            return redirect('gestion_canchas')
    else:
        form = CanchaForm(instance=cancha)
    return render(request, 'canchas/form_cancha.html', {'form': form, 'titulo': f'Modificar Cancha: {cancha.codigo}'})

@login_required
@user_passes_test(es_staff)
def eliminar_cancha(request, pk):
    cancha = get_object_or_404(Cancha, pk=pk)
    if request.method == 'POST':
        # Mecanismo de baja lógica exigido por el Módulo 1 para no destruir datos físicamente
        cancha.activo = False
        cancha.save()
        messages.warning(request, f"La cancha {cancha.codigo} ha sido dada de baja del catálogo.")
        return redirect('gestion_canchas')
    return render(request, 'canchas/confirmar_eliminar.html', {'cancha': cancha})


# --- AUTENTICACIÓN ---

def login_usuario(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('catalogo_publico')
    else:
        form = AuthenticationForm()
    return render(request, 'canchas/login.html', {'form': form})

def logout_usuario(request):
    logout(request)
    return redirect('catalogo_publico')
