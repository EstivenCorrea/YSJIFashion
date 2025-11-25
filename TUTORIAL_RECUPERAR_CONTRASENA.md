# 🎬 TUTORIAL: Sistema de Recuperación de Contraseña

## 📸 Paso a Paso para Configurar

### **1️⃣ CONFIGURAR GMAIL - 5 MINUTOS**

#### A) Ir a Google Account Security
1. Abre: https://myaccount.google.com/
2. Haz clic en "Seguridad" (lado izquierdo)
3. Busca "Contraseña de aplicación"

#### B) Generar Contraseña de Aplicación
1. Selecciona:
   - Aplicación: **Mail**
   - Dispositivo: **Windows**
2. Haz clic en "Generar"
3. **COPIA la contraseña** (16 caracteres con espacios)

```
Ejemplo: xxxx xxxx xxxx xxxx
```

---

### **2️⃣ CREAR ARCHIVO .env**

#### En la carpeta raíz (`YSJI-main/`):

**Windows (PowerShell):**
```powershell
copy .env.example .env
```

**Linux/Mac:**
```bash
cp .env.example .env
```

#### Edita `.env` con tu editor:

```
EMAIL_USER=Yjsifashion@gmail.com
EMAIL_PASS=xxxx xxxx xxxx xxxx
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
```

**⚠️ Importante:** 
- Reemplaza `xxxx xxxx xxxx xxxx` con la contraseña copiada
- **No compartas el archivo `.env`**
- Agrega `.env` a `.gitignore` para no subirlo a Git

---

### **3️⃣ EJECUTAR MIGRACIONES**

En la terminal, dentro de la carpeta del proyecto:

```bash
python manage.py migrate core
```

Deberías ver:
```
Applying core.0004_add_token_recuperacion... OK
```

---

### **4️⃣ INICIAR EL SERVIDOR**

```bash
python manage.py runserver
```

Deberías ver:
```
Starting development server at http://127.0.0.1:8000/
```

---

## 🧪 PROBAR EL SISTEMA

### **Escenario 1: Cambiar Contraseña**

#### OPCIÓN A: Si ya tienes usuario
1. Abre: http://localhost:8000/login/
2. Haz clic en: **"¿Olvidaste tu contraseña?"**
3. Ingresa tu correo
4. Haz clic: **"Enviar enlace"**
5. Revisa bandeja de entrada o SPAM
6. Haz clic en el enlace del correo
7. Ingresa nueva contraseña (mínimo 6 caracteres)
8. Haz clic: **"Guardar"**
9. ¡Listo! Inicia sesión con tu nueva contraseña

#### OPCIÓN B: Crear usuario de prueba
1. Abre: http://localhost:8000/login/
2. Haz clic: **"Regístrate"**
3. Rellena:
   - Nombre: `Juan Pérez`
   - Correo: `tu_correo@gmail.com`
   - Contraseña: `123456`
4. Haz clic: **"Crear Cuenta"**
5. Ahora repite los pasos de la OPCIÓN A

---

## 📧 ¿DÓNDE VER EL CORREO?

### **En Producción (Gmail Real)**
- Revisa tu bandeja de entrada normalmente
- Si no llega, revisa carpeta **SPAM**

### **En Desarrollo (Terminal)**
Si usas `python manage.py runserver`, el correo aparece en la terminal:

```
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Recuperar contraseña - YSJI Fashion
From: Yjsifashion@gmail.com
To: usuario@example.com
Date: ...

Hola Juan,

Recibimos una solicitud para recuperar tu contraseña...

Para restaurar tu contraseña, haz clic aquí:
http://localhost:8000/password-reset-confirm/1/550e8400-e29b-41d4-a716-446655440000/

Este enlace expira en 24 horas.

Saludos,
Equipo YSJI Fashion
```

**Copia el enlace desde la terminal y abre en el navegador.**

---

## ❌ SOLUCIONAR PROBLEMAS

### **Problema 1: "ERROR: ModuleNotFoundError: No module named 'dotenv'"**

**Solución:**
```bash
pip install python-dotenv
```

---

### **Problema 2: "No recibo correo en producción"**

**Checklist:**
- ✅ Credenciales en `.env` son correctas
- ✅ El correo existe en Gmail
- ✅ Revisar carpeta SPAM
- ✅ Revisar que `.env` esté en la carpeta raíz (no en subcarpetas)
- ✅ Reiniciar servidor después de cambiar `.env`

---

### **Problema 3: "Token inválido o expirado"**

**Causas:**
- El token pasó más de 24 horas
- El token ya fue usado
- El URL se copió incorrectamente

**Solución:**
- Solicitar un nuevo enlace de recuperación

---

### **Problema 4: "Error al actualizar contraseña"**

**Validar:**
- ✅ Contraseña tiene mínimo 6 caracteres
- ✅ Ambas contraseñas coinciden
- ✅ Sin caracteres especiales problemáticos

---

## 🔍 VERIFICAR QUE TODO FUNCIONA

### **Check 1: Base de Datos**
```bash
python manage.py shell
```

```python
from core.models import TokenRecuperacion
print(TokenRecuperacion.objects.all())
# Deberías ver: <QuerySet []>
```

### **Check 2: Rutas**
```bash
python manage.py show_urls | grep password
```

Deberías ver:
```
password_reset     /password-reset/
password_reset_confirm    /password-reset-confirm/<int:uidb64>/<str:token>/
```

### **Check 3: Configuración de Email**
```bash
python manage.py shell
```

```python
from django.conf import settings
print(settings.EMAIL_HOST)  # smtp.gmail.com
print(settings.EMAIL_PORT)  # 587
print(settings.EMAIL_USE_TLS)  # True
```

---

## 📊 RESUMEN TÉCNICO

| Aspecto | Detalle |
|---------|---------|
| **Base de Datos** | Tabla `token_recuperacion` en MySQL |
| **Validez del Token** | 24 horas |
| **Encriptación de Contraseña** | PBKDF2 (Django estándar) |
| **Correo SMTP** | Gmail con App Password |
| **URL Segura** | HTTPS (recomendado en producción) |
| **CSRF** | Protegido con token CSRF |

---

## 🎯 FLUJO COMPLETO TÉCNICO

```
┌─────────────────────────────────────────────┐
│ Usuario accede a /login/                    │
│ Haz clic en "¿Olvidaste tu contraseña?"    │
└─────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────┐
│ GET /password-reset/                        │
│ Sistema muestra formulario                  │
└─────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────┐
│ Usuario ingresa correo y haz clic enviar   │
│ POST /password-reset/ (AJAX)               │
└─────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────┐
│ Sistema:                                    │
│ 1. Busca usuario con ese correo            │
│ 2. Genera token único (UUID)               │
│ 3. Fija expiración: ahora + 24 horas      │
│ 4. Guarda en BD tabla token_recuperacion   │
│ 5. Arma URL con id de usuario y token     │
│ 6. Envía correo con el URL                 │
└─────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────┐
│ Usuario recibe correo y hace clic en URL   │
│ GET /password-reset-confirm/1/abc123/     │
└─────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────┐
│ Sistema:                                    │
│ 1. Busca el token en BD                    │
│ 2. Valida que no haya expirado            │
│ 3. Valida que no fue usado                 │
│ 4. Muestra formulario                      │
└─────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────┐
│ Usuario ingresa nueva contraseña           │
│ POST /password-reset-confirm/1/abc123/    │
└─────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────┐
│ Sistema:                                    │
│ 1. Valida que las contraseñas coincidan   │
│ 2. Valida mínimo 6 caracteres             │
│ 3. Encripta con PBKDF2                    │
│ 4. Guarda en BD tabla usuarios            │
│ 5. Marca token como usado                 │
│ 6. Redirige a login                       │
└─────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────┐
│ Usuario inicia sesión con nueva contraseña │
│ ✅ ¡ÉXITO!                                 │
└─────────────────────────────────────────────┘
```

---

## 💡 TIPS ÚTILES

1. **Para testing**: En desarrollo, los correos aparecen en terminal
2. **Para producción**: Usar HTTPS obligatoriamente
3. **Para seguridad**: Cambiar contraseña regularmente
4. **Para mantenimiento**: Limpiar tokens expirados periódicamente

---

## 📞 SOPORTE TÉCNICO

Si algo no funciona:

1. Revisar la consola del servidor Django
2. Verificar que `.env` existe y tiene valores correctos
3. Revisar logs de errores de MySQL
4. Limpiar cache del navegador (Ctrl+Shift+Del)

---

**¡Listo! Tu sistema de recuperación de contraseña está funcionando.** 🎉

