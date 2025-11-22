from django.dispatch import receiver
from allauth.account.signals import user_signed_up, user_logged_in, user_logged_out
from allauth.socialaccount.signals import social_account_added, social_account_updated
from .models import Usuario
from django.contrib import messages
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import os
from django.utils.crypto import get_random_string


def _create_or_update_usuario_from_social(user, sociallogin):
    """
    Crea o actualiza una instancia de core.Usuario a partir de la información
    del sociallogin (Google). `user` es el User de Django provisto por allauth.
    """
    extra_data = {}
    try:
        extra_data = sociallogin.account.extra_data
    except Exception:
        extra_data = {}

    email = extra_data.get('email') or getattr(user, 'email', None)
    nombre = extra_data.get('name') or extra_data.get('given_name') or getattr(user, 'first_name', '') or user.username
    imagen = None
    # Google provider suele devolver 'picture'
    imagen = extra_data.get('picture')

    if not email:
        return None

    usuario, created = Usuario.objects.get_or_create(correo=email, defaults={
        'nombre': nombre,
        'correo': email,
    })

    # Actualizar nombre si cambió
    updated = False
    if usuario.nombre != nombre:
        usuario.nombre = nombre
        updated = True

    # Si Google proporciona una URL de imagen, intentar descargar y guardar
    if imagen:
        try:
            # Si la imagen ya fue almacenada (y no es una URL), evitamos descargar de nuevo
            current = getattr(usuario, 'imagen_perfil')
            need_download = True
            if current and hasattr(current, 'url'):
                # comparar URLs simples (si se almacenó vía URL previamente, puede variar)
                if imagen in current.url:
                    need_download = False

            if need_download:
                # descargar contenido
                try:
                    resp = urlopen(imagen)
                    image_data = resp.read()
                    # generar nombre de archivo único
                    ext = os.path.splitext(imagen.split('?')[0])[1] or '.jpg'
                    filename = f'perfiles/{get_random_string(12)}{ext}'
                    # guardar en storage
                    default_storage.save(filename, ContentFile(image_data))
                    # eliminar imagen anterior si existía y es distinta
                    try:
                        old = getattr(usuario, 'imagen_perfil')
                        old_name = getattr(old, 'name', None)
                        if old_name and old_name != filename:
                            # borrar archivo antiguo
                            default_storage.delete(old_name)
                    except Exception:
                        pass
                    # asignar al campo imagen_perfil (asumiendo ImageField)
                    usuario.imagen_perfil = filename
                    updated = True
                except (HTTPError, URLError):
                    pass
        except Exception:
            pass

    if updated:
        usuario.save()

    return usuario


@receiver(user_signed_up)
def handle_user_signed_up(request, user, **kwargs):
    """Se dispara cuando allauth crea un User (signup normal o social)."""
    sociallogin = kwargs.get('sociallogin')
    if sociallogin:
        usuario = _create_or_update_usuario_from_social(user, sociallogin)
        if usuario and request is not None:
            # Crear sesión para mantener compatibilidad con el proyecto actual
            request.session['usuario_id'] = usuario.id
            request.session['usuario_nombre'] = usuario.nombre
            request.session['usuario_rol'] = usuario.rol
            # Pedir al usuario que cambie su contraseña desde la vista de cuenta
            try:
                messages.warning(request, 'Importante: cambia tu contraseña desde esta sección para mayor seguridad.')
            except Exception:
                pass


@receiver(user_logged_in)
def handle_user_logged_in(request, user, **kwargs):
    """Se dispara cuando un usuario hace login (social o tradicional).
    Aseguramos que exista una fila en `Usuario` y que la sesión tenga
    las claves que usa el resto del proyecto (`usuario_id`, etc.).
    """
    sociallogin = kwargs.get('sociallogin')
    usuario = None
    if sociallogin:
        usuario = _create_or_update_usuario_from_social(user, sociallogin)
    else:
        # intentar vincular por correo con el modelo Usuario existente
        try:
            usuario = Usuario.objects.filter(correo__iexact=getattr(user, 'email', '')).first()
        except Exception:
            usuario = None

    if usuario and request is not None:
        request.session['usuario_id'] = usuario.id
        request.session['usuario_nombre'] = usuario.nombre
        request.session['usuario_rol'] = usuario.rol
        # Si el login viene de social, advertir al usuario
        if sociallogin:
            try:
                messages.warning(request, 'Importante: cambia tu contraseña desde esta sección para mayor seguridad.')
            except Exception:
                pass


@receiver(user_logged_out)
def handle_user_logged_out(request, user, **kwargs):
    """Limpiar la sesión personalizada cuando el usuario hace logout."""
    if request is not None:
        request.session.pop('usuario_id', None)
        request.session.pop('usuario_nombre', None)
        request.session.pop('usuario_rol', None)


@receiver(social_account_added)
def handle_social_account_added(request, sociallogin, **kwargs):
    # Cuando se añade una cuenta social a un usuario ya existente
    user = sociallogin.user
    usuario = _create_or_update_usuario_from_social(user, sociallogin)
    if usuario and request is not None:
        request.session['usuario_id'] = usuario.id
        request.session['usuario_nombre'] = usuario.nombre
        request.session['usuario_rol'] = usuario.rol


@receiver(social_account_updated)
def handle_social_account_updated(request, sociallogin, **kwargs):
    user = sociallogin.user
    _create_or_update_usuario_from_social(user, sociallogin)
