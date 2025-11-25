# 📝 Sistema de Recuperación de Contraseña - YSJI Fashion

## ✅ Implementación Completada

El sistema de "Recordar/Recuperar Contraseña" ha sido implementado correctamente. Aquí está todo lo que se ha hecho:

---

## 🔧 Cambios Realizados

### 1. **Modelo de Base de Datos** (`core/models.py`)
Se agregó el modelo `TokenRecuperacion`:
- Almacena tokens únicos para recuperación de contraseña
- Cada token es válido por **24 horas**
- Registra cuándo se creó y expira
- Marca si el token ya fue usado (para evitar reuso)

```python
class TokenRecuperacion(models.Model):
    usuario_id = models.IntegerField()
    token = models.CharField(max_length=255, unique=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    expira_en = models.DateTimeField()
    usado = models.BooleanField(default=False)
```

---

### 2. **Vistas (Backend)** (`core/views.py`)

#### **a) Vista: `password_reset`**
- Maneja la solicitud inicial de recuperación
- **GET**: Muestra formulario para ingresar correo
- **POST (AJAX)**: 
  - Valida que el usuario exista
  - Genera un token de 24 horas
  - Envía correo con enlace de recuperación
  - Responde con JSON (compatible con SweetAlert2)

#### **b) Vista: `password_reset_confirm`**
- Maneja el cambio de contraseña
- **GET**: Valida el token y muestra formulario para nueva contraseña
- **POST (AJAX)**:
  - Valida que las contraseñas coincidan
  - Mínimo 6 caracteres
  - Encripta y guarda la nueva contraseña
  - Marca el token como usado

---

### 3. **Rutas (URLs)** (`core/urls.py`)

```python
path('password-reset/', views.password_reset, name='password_reset'),
path('password-reset-confirm/<int:uidb64>/<str:token>/', 
     views.password_reset_confirm, name='password_reset_confirm'),
```

---

### 4. **Configuración de Correo** (`ysjifashion/settings.py`)

✅ **Ya estaba configurada:**
- Servidor SMTP: Gmail (`smtp.gmail.com`)
- Puerto TLS: 587
- Credenciales desde variables de entorno (`.env`)
- Email de remitente: `Yjsifashion@gmail.com`

**⚠️ Requiere:**
1. Crear archivo `.env` en la raíz del proyecto:
```
EMAIL_USER=Yjsifashion@gmail.com
EMAIL_PASS=tu_app_password_gmail
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
```

2. Generar "App Password" de Gmail:
   - Ir a: https://myaccount.google.com/apppasswords
   - Seleccionar: Mail + Windows
   - Copiar la contraseña generada
   - Guardar en `.env`

---

### 5. **Plantilla HTML** (`core/templates/password_reset.html`)

#### **Paso 1: Solicitar Correo**
- Formulario simple para ingresar correo
- Envío AJAX sin recargar página
- Mensajes con SweetAlert2

#### **Paso 2: Cambiar Contraseña**
- Valida el token
- Muestra error si el token expiró
- Formulario para nueva contraseña
- Validación en cliente y servidor

---

### 6. **CSS Responsive** (`core/static/css/password_reset.css`)
- Diseño moderno con gradientes
- Completamente responsivo
- Compatible con móviles

---

### 7. **Base de Datos - Migración**
```bash
python manage.py makemigrations core
python manage.py migrate core
```

Crea tabla `token_recuperacion` en MySQL.

---

## 🚀 Cómo Usar

### **Paso 1: Preparar Variables de Entorno**
Crea archivo `.env` en la raíz:
```
EMAIL_USER=Yjsifashion@gmail.com
EMAIL_PASS=tu_app_password_generado
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
```

### **Paso 2: Usuarios Finales**

1. **Ir a Login**: http://localhost:8000/login/
2. **Hacer clic en**: "¿Olvidaste tu contraseña?"
3. **Ingresar correo** y hacer clic en "Enviar enlace"
4. **Revisar bandeja de entrada** (o spam)
5. **Hacer clic en el enlace** del correo
6. **Crear nueva contraseña** (mínimo 6 caracteres)
7. **Listo**: Puedes iniciar sesión con la nueva contraseña

---

## 🔐 Características de Seguridad

✅ Tokens únicos con UUID  
✅ Expiración automática (24 horas)  
✅ Tokens de un solo uso  
✅ Contraseñas encriptadas con PBKDF2  
✅ Validación en servidor (no solo cliente)  
✅ CSRF protection  
✅ Mensajes genéricos (no revela si email existe)  

---

## 📧 Flujo del Correo

```
Usuario solicita recuperación
        ↓
Sistema valida email
        ↓
Genera token único (24h válido)
        ↓
Envía correo con enlace
        ↓
Usuario hace clic en enlace
        ↓
Valida token
        ↓
Usuario ingresa nueva contraseña
        ↓
Sistema encripta y guarda
        ↓
Marca token como usado
        ↓
Redirige a login
```

---

## 🧪 Pruebas

### Test Manual:
```bash
# 1. Crear un usuario de prueba
http://localhost:8000/login/  # Registrarse

# 2. Ir a recuperar contraseña
http://localhost:8000/password-reset/

# 3. Ingresar el correo del usuario

# 4. Revisar correos (terminal en modo debug muestra el enlace)

# 5. Hacer clic en el enlace del correo

# 6. Cambiar contraseña

# 7. Iniciar sesión con nueva contraseña
```

---

## 📋 Checklist Final

- [x] Modelo `TokenRecuperacion` creado
- [x] Vistas `password_reset` y `password_reset_confirm` implementadas
- [x] Rutas registradas
- [x] Configuración de correo SMTP lista
- [x] Plantilla HTML mejorada
- [x] CSS responsive
- [x] Migración aplicada
- [x] Enlace en login ("¿Olvidaste tu contraseña?")
- [x] Seguridad: tokens únicos, expiración, un solo uso
- [x] Mensajes AJAX con SweetAlert2
- [x] Validación en cliente y servidor

---

## 📞 Soporte

Si tienes problemas:

1. **Correo no llega**: 
   - Revisar credenciales en `.env`
   - Revisar carpeta SPAM
   - En desarrollo, el enlace aparece en la terminal

2. **Token inválido**:
   - El token solo es válido 24 horas
   - Debe usarse una sola vez
   - Solicitar un nuevo enlace si expiró

3. **Contraseña no cambia**:
   - Mínimo 6 caracteres
   - Las contraseñas deben coincidir
   - Verificar consola del servidor para errores

---

**¡Sistema de Recuperación de Contraseña funcional y seguro!** ✨
