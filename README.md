# EVALUACIÓN SUMATIVA N° 3
**Asignatura:** Programación Back End (TI3041)  
**Unidad 2:** Framework Back End (Django)  
**Ponderación:** 30% de la nota final  

---

## 1. Ficha de Registro y Aprobación de la Propuesta
* **Nombre de la Organización:** MatchPoint Pro
* **Modelo de Negocio / Giro:** Complejo deportivo de arriendo de canchas polideportivas y servicios anexos.
* **Integrantes del Equipo:** Omar Barriga - RUT: 21.920.674-7
* **Entidad de Contexto / Agrupación (ORM):** `Disciplina` (Pádel, Tenis, Fútbol, Básquetbol)
* **Entidad Principal Gestionable (ORM):** `Cancha` (Código alfanumérico único, tarifa por bloque, superficie, estado, imagen)
* **Propósito de la Sesión (request.session):** **Reserva de Jornada**: Mecanismo de acumulación y manipulación transitoria en memoria de sesión para la selección de bloques horarios e implementos deportivos adicionales, aplicando cálculos matemáticos con desglose de Neto, IVA (19%) y Total General.

---

## 2. Instrucciones de Despliegue Local (Paso a Paso)

Siga este orden estricto en la terminal de PowerShell para levantar y evaluar la plataforma:

### Paso 1: Configurar el Directorio de Trabajo e Instalar Dependencias
```powershell
cd C:\Users\chilab\Desktop\matchpoint_pro
python -m venv .venv
.venv\Scripts\pip install django pillow python-dotenv
```

### Paso 2: Inicializar el Entorno de Django
```powershell
.venv\Scripts\django-admin startproject config .
.venv\Scripts\python manage.py startapp canchas
```

### Paso 3: Ejecutar Migraciones del Modelo de Datos
```powershell
.venv\Scripts\python manage.py makemigrations
.venv\Scripts\python manage.py migrate
```

### Paso 4: Poblado Automatizado de la Base de Datos (Módulo 1.4)
Se diseñó un comando personalizado para inyectar los datos semilla requeridos:
```powershell
.venv\Scripts\python manage.py poblar_datos
```

### Paso 5: Ejecución del Servidor Local
```powershell
.venv\Scripts\python manage.py runserver
```
* **Acceso Público:** http://127.0.0
* **Acceso Backoffice Protegido:** http://127.0.0admin/ (Usuario: `admin` | Clave: `admin123`)

---

## 3. Verificación de Pilares Obligatorios Cumplidos
1. **Aislamiento y Seguridad:** Variables desacopladas en `.env` mediante `python-dotenv`. Archivos temporales excluidos mediante `.gitignore`.
2. **Capa de Datos ORM:** Uso de `models.PROTECT` para integridad referencial y `MinValueValidator(0)` para denegar tarifas negativas.
3. **Panel Operativo a Medida:** Identidad corporativa corporativizada y grillas de datos con edición rápida (`list_editable`).
4. **Manejo de Sesión Volátil:** Operaciones matemáticas complejas calculadas dinámicamente en `request.session` sin persistencia inmediata.

---

## 🤖 4. Bitácora de Uso Técnico y Ético de Inteligencia Artificial (Módulo 4)

En cumplimiento con las directrices institucionales, se documenta la asistencia técnica de IA en el desarrollo del backend:

### Caso 1: Optimización de Consultas Relacionales (ORM)
*   **Prompt Utilizado:** *"¿Cómo puedo optimizar una consulta en Django ORM para un catálogo público que tiene una relación ForeignKey hacia otra tabla y evitar el problema de N+1 consultas?"*
*   **Respuesta Técnica:** Se sugirió el uso del método `.select_related('disciplina')` para realizar un `JOIN` SQL directo en la base de datos.
*   **Adaptación:** Se implementó directamente en la vista `catalogo_publico` y en el listado del backoffice de `views.py`.

### Caso 2: Seguridad en Formularios Web (ModelForm)
*   **Prompt Utilizado:** *"Necesito crear un formulario ModelForm en Django que valide que un código alfanumérico no esté duplicado al editar y que un valor entero no sea negativo usando métodos clean."*
*   **Respuesta Técnica:** La IA estructuró los métodos específicos `clean_codigo()` y `clean_tarifa_bloque()` levantando excepciones del tipo `forms.ValidationError`.
*   **Adaptación:** Bloque integrado por completo en el archivo `canchas/forms.py` para blindar la operación Create y Update.

### Caso 3: Control de Estado In-Memory (request.session)
*   **Prompt Utilizado:** *"¿Cómo estructurar un diccionario dentro de request.session en Django para almacenar un itinerario temporal con desgloses matemáticos de IVA (19%) sin persistencia en base de datos?"*
*   **Respuesta Técnica:** Explicación del comportamiento de serialización JSON de las sesiones de Django y la obligatoriedad de marcar la sesión como modificada o reasignar el diccionario.
*   **Adaptación:** Lógica aplicada en las funciones `agregar_a_jornada` y `ver_jornada` dentro de las vistas de negocio.
