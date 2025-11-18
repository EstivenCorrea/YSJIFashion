from decimal import Decimal
from django.db import transaction
from django.db.models import F
from django.utils import timezone

def calcular_precio_con_descuento(precio_base: Decimal, descuento) -> Decimal:
    if descuento is None:
        return precio_base
    if not descuento.vigente(timezone.now()):
        return precio_base
    if descuento.tipo == 'porcentaje':
        monto = (precio_base * (descuento.valor / Decimal('100'))).quantize(Decimal('0.01'))
    else:
        monto = descuento.valor
    precio_final = precio_base - monto
    return max(precio_final, Decimal('0.00'))

def consumir_descuento_seguro(descuento, cantidad_usos=1):
    """Incrementa usos_realizados de forma segura (usa transacción)."""
    # Llamar dentro de una transacción principal del pedido
    if descuento is None:
        return
    descuento.refresh_from_db()
    if descuento.max_uso is not None and descuento.usos_realizados + cantidad_usos > descuento.max_uso:
        raise ValueError("El descuento ha alcanzado el número máximo de usos.")
    descuento.usos_realizados = F('usos_realizados') + cantidad_usos
    descuento.save()
    descuento.refresh_from_db()
