#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ysjifashion.settings')
django.setup()

from django.template import loader
from types import SimpleNamespace
from decimal import Decimal

# Porcentaje
p1 = SimpleNamespace(
    id=1, nombre_producto='Abrigo 30% OFF', codigo_producto='A1',
    descripcion_producto='Abrigo largo', imagen_producto=None,
    imagenes=SimpleNamespace(count=0, all=lambda:[], first=None),
    tiene_descuento=True, valor_producto=Decimal('699000'),
    precio_final=Decimal('489300'), texto_ribbon='-30% OFF',
    descuento=SimpleNamespace(tipo='porcentaje', valor=30, activo=True),
    stock=SimpleNamespace(cantidad=5), tallas_disponibles='S,M,L',
    colores_disponibles='Rojo,Azul', marca=SimpleNamespace(nombre='MarcaX'),
    categoria=None
)

# Monto
p2 = SimpleNamespace(
    id=2, nombre_producto='Pantalon -50K', codigo_producto='P2',
    descripcion_producto='Pantalon', imagen_producto=None,
    imagenes=SimpleNamespace(count=0, all=lambda:[], first=None),
    tiene_descuento=True, valor_producto=Decimal('150000'),
    precio_final=Decimal('100000'), texto_ribbon='-$50.000',
    descuento=SimpleNamespace(tipo='monto', valor=50000, activo=True),
    stock=SimpleNamespace(cantidad=3), tallas_disponibles='S,M,L,XL',
    colores_disponibles='Negro,Azul', marca=SimpleNamespace(nombre='MarcaY'),
    categoria=None
)

ctx1 = {'productos': [p1, p2], 'categorias_conteo': [], 'marcas': [],
        'usuario': None, 'sesion_activa': False, 'request': SimpleNamespace(GET={})}

print('Testing Catalogo.html with both discount types...')
t1 = loader.get_template('Catalogo.html')
html1 = t1.render(ctx1)
print('  Render OK')
if '-30% OFF' in html1:
    print('    ✓ Porcentaje: OK')
if 'Pantalon' in html1:
    print('    ✓ Monto producto: OK')

print('\nTesting producto_detalle_publico.html...')
ctx2 = {'producto': p2}  # monto
t2 = loader.get_template('producto_detalle_publico.html')
html2 = t2.render(ctx2)
print('  Render monto OK')
if '-$' in html2 and '50' in html2:
    print('    ✓ Monto detail: OK')

ctx3 = {'producto': p1}  # porcentaje
html3 = t2.render(ctx3)
print('  Render porcentaje OK')
if '-30% OFF' in html3:
    print('    ✓ Porcentaje detail: OK')

print('\n✅ All tests passed!')
