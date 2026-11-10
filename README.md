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
.venv\Scripts\activate
pip install django pillow python-dotenv
```

### Paso 2: Inicializar el Entorno de Django y la Aplicación
```powershell
django-admin startproject config .
python manage.py startapp canchas
```

### Paso 3: Ejecutar Migraciones del Modelo de Datos
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Paso 4: Poblado Automatizado de la Base de Datos (Módulo 1.4)
Se diseñó un comando personalizado para inyectar los datos semilla requeridos (4 disciplinas y 8 canchas operativas):
```powershell
python manage.py poblar_datos
```

### Paso 5: Ejecución del Servidor Local
```powershell
python manage.py runserver
```
* **Acceso Público:** http://127.0.0
* **Acceso Backoffice Protegido:** http://127.0.0admin/ (Usuario: `admin` | Clave: `admin123`)

---

## 3. Verificación de Pilares Obligatorios Cumplidos
1. **Aislamiento y Seguridad:** Variables desacopladas en `.env` mediante `python-dotenv`. Archivos temporales, bases de datos y carpetas multimedia excluidos mediante `.gitignore`.
2. **Capa de Datos ORM:** Uso de `models.PROTECT` para integridad referencial en disciplinas y `MinValueValidator(0)` para denegar tarifas negativas en canchas.
3. **Panel Operativo a Medida:** Identidad corporativa personalizada en `admin.py` y grillas de datos optimizadas con filtros laterales y edición rápida (`list_editable`).
4. **Manejo de Sesión Volátil:** Operaciones matemáticas complejas calculadas dinámicamente en `request.session` sin persistencia inmediata para simular el cotizador de jornadas.

---

## 🤖 4. Bitácora de Uso Técnico y Ético de Inteligencia Artificial (Módulo 4)

En cumplimiento con el criterio de **utilización asistida de IA**, se documenta la trazabilidad del desarrollo colaborativo entre el estudiante y el asistente de IA, detallando la resolución de bugs arquitectónicos durante la sesión de codificación:

### Caso 1: Diagnóstico de Rutas y Estructura de Carpetas en Django
*   **Problemática / Error:** Django lanzaba errores de renderizado y no encontraba las plantillas HTML debido a que VS Code colapsaba la vista visual de directorios vacíos mediante *Compact Folders* (ayuda visual que unía los nombres de carpetas consecutivas con barras invertidas `templates\canchas`), sumado a un desajuste en la configuración de la tupla `DIRS` en el archivo `settings.py`.
*   **Prompt Utilizado:** *"Al crear mi carpeta de plantillas en la raíz de mi proyecto de Django, VS Code la agrupa visualmente en una sola línea como 'templates\canchas' y el servidor no me reconoce las vistas de mis HTML. ¿Qué está fallando en la arquitectura de mis carpetas o en mi settings.py?"*
*   **Respuesta de la IA:** Explicó que el editor colapsa visualmente rutas secuenciales cuando no tienen archivos hermanos directos en la raíz, pero advirtió que la tupla de configuración del motor de plantillas en `settings.py` debía apuntar dinámicamente usando `BASE_DIR / 'templates'` para que Django rastreara correctamente el árbol exterior.
*   **Adaptación/Solución:** Se corrigió el bloque `TEMPLATES` en `config/settings.py` para mapear la ruta global y se validó físicamente la separación jerárquica de los directorios.

### Caso 2: Inyección de Estilos Locales Seguros contra Bloqueos de Red (Falla de CDN)
*   **Problemática / Error:** Al importar los estilos de Bootstrap 5 mediante servidores CDN tradicionales (`jsdelivr` / `cdnjs`), los proxies locales o filtros de red de la terminal de la institución educativa bloqueaban y recortaban las URLs de los archivos `.css`, dejando la aplicación web completamente plana (hoja en blanco sin estilos).
*   **Prompt Utilizado:** *"Los enlaces CDN oficiales de Bootstrap 5 no cargan en mis templates de Django debido a restricciones del entorno de red de mi laboratorio, rompiendo toda la interfaz responsiva. ¿Cómo puedo asegurar el diseño visual de Bootstrap sin depender de peticiones externas o internet?"*
*   **Respuesta de la IA:** Sugirió inyectar las clases y estilos utilitarios esenciales de Bootstrap (estructuras de grillas, diseño de tarjetas, tipografía y badges dinámicos) incrustándolos directamente dentro de etiquetas nativas `<style>` en la cabecera de cada plantilla HTML.
*   **Adaptación/Solución:** Se reescribieron las plantillas `catalogo.html` y `jornada.html` con una capa CSS embebida que emula los componentes de Bootstrap 5, asegurando el renderizado inmediato sin conexiones externas.

### Caso 3: Seguridad en Formularios Web (ModelForm) y Evitación de Duplicados
*   **Prompt Utilizado:** *"Necesito crear un formulario ModelForm en Django que valide que un código alfanumérico no esté duplicado al editar y que un valor entero no sea negativo usando métodos clean."*
*   **Respuesta de la IA:** Estructuró los métodos específicos `clean_codigo()` y `clean_tarifa_bloque()` levantando excepciones del tipo `forms.ValidationError` para interceptar datos anómalos antes de que lleguen a la base de datos.
*   **Adaptación/Solución:** Bloque integrado por completo en el archivo `canchas/forms.py` para blindar las operaciones de creación y actualización en el frontend.

### Caso 4: Control de Estado In-Memory (request.session) y Aislamiento de Clientes
*   **Prompt Utilizado:** *"¿Cómo estructurar un diccionario dentro de request.session en Django para almacenar un itinerario temporal con desgloses matemáticos de IVA (19%) sin persistencia en base de datos?"*
*   **Respuesta de la IA:** Explicó el comportamiento de serialización JSON de las sesiones de Django y cómo el `SessionMiddleware` asocia un hash único en una cookie por cada navegador, garantizando que el planificador de un cliente sea inaccesible para otro.
*   **Adaptación/Solución:** Lógica implementada en las vistas `agregar_a_jornada` y `ver_jornada` dentro de `canchas/views.py` para aislar el flujo de cálculo económico de Neto, IVA y Total.
