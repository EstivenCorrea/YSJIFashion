from django.contrib import admin
from .models import Descuento, Producto

@admin.register(Descuento)
class DescuentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'tipo', 'valor', 'activo', 'fecha_inicio', 'fecha_fin')
    list_filter = ('activo', 'tipo')
    search_fields = ('nombre', 'codigo')
    ordering = ('-creado_en',)

# core/admin.py
from django.contrib import admin
from .models import Producto, Categoria, Marca, Proveedor, Descuento

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'codigo_producto',
        'nombre_producto',
        'valor_producto',      # antes referías list_display[3] -> 'cantidad_producto' (lo quitamos)
        'categoria',           # muestra la FK
        'marca',
        'proveedor',
        'descuento',
    )
    list_filter = (
        'categoria',   # antes 'categoria_producto'
        'marca',
        'proveedor',
        'descuento',
    )
    search_fields = ('nombre_producto', 'codigo_producto')
    ordering = ('-id',)
