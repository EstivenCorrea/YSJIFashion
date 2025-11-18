from django.db import models, transaction
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    correo = models.CharField(max_length=100, unique=True)
    imagen_perfil = models.ImageField(upload_to='perfiles/', null=True, blank=True)
    contraseña = models.CharField(max_length=255)

    ADMIN = 'admin'
    USUARIO = 'usuario'

    ROLES = [
        (ADMIN, 'Admin'),
        (USUARIO, 'Usuario'),
    ]

    rol = models.CharField(max_length=20, choices=ROLES, default=USUARIO)
    fecha_creacion = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'usuarios'


class Pedido(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    productos = models.JSONField()
    estado = models.CharField(max_length=20, default='Pendiente')
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'pedidos'

    @property
    def total(self):
            total = 0
            for item in self.productos:
                precio = item.get("precio", 0)
                cantidad = item.get("cantidad", 1)
                total += precio * cantidad
            return total



class Descuento(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=50, null=True)
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(null=True)
    tipo = models.CharField(max_length=20, default='porcentaje')
    valor = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    max_uso = models.IntegerField(null=True)
    usos_realizados = models.IntegerField(default=0)
    aplicable_a = models.CharField(max_length=30, default='todos')
    fecha_inicio = models.DateTimeField(null=True)
    fecha_fin = models.DateTimeField(null=True)
    activo = models.BooleanField(default=True)
    observaciones = models.TextField(null=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False  # 👉 Importante: Django no creará la tabla
        db_table = 'descuentos'  # nombre real de tu tabla MySQL
        ordering = ['-creado_en']

    def __str__(self):
        return f"{self.nombre} ({self.valor}{'%' if self.tipo == 'porcentaje' else '$'})"



from django.utils import timezone
from decimal import Decimal
class Producto(models.Model):

    codigo_producto   = models.CharField(max_length=100, unique=True)
    nombre_producto   = models.CharField(max_length=200)
    descripcion_producto = models.TextField()
    valor_producto    = models.DecimalField(max_digits=10, decimal_places=2)
    # ahora usamos la tabla `Categoria` como FK en lugar de choices
    categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null=True, blank=True, related_name='productos')
    imagen_producto   = models.ImageField(upload_to='productos/', blank=True, null=True)
    tallas_disponibles = models.CharField(max_length=100, null=True)
    colores_disponibles = models.CharField(max_length=100, null=True)
    marca = models.ForeignKey('Marca', on_delete=models.SET_NULL, null=True, blank=True)
    proveedor = models.ForeignKey('Proveedor', on_delete=models.SET_NULL, null=True, blank=True)

    descuento = models.ForeignKey(
    'Descuento',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    db_column='descuento_id',
    related_name='productos'
)
    # --- MÉTODOS PARA MANEJO DE DESCUENTO ---
    @property
    def tiene_descuento(self):
        """Valida si el producto tiene un descuento válido y vigente."""
        if not self.descuento:
            return False
        if not self.descuento.activo:
            return False
        if self.descuento.fecha_inicio and self.descuento.fecha_inicio > timezone.now():
            return False
        if self.descuento.fecha_fin and self.descuento.fecha_fin < timezone.now():
            return False
        return True

    @property
    def valor_descuento(self):
        """Retorna el valor del descuento según el tipo."""
        if not self.tiene_descuento:
            return Decimal('0.00')

        if self.descuento.tipo == "porcentaje":
            try:
                vp = Decimal(str(self.valor_producto))
                dv = Decimal(str(self.descuento.valor))
                return (vp * dv) / Decimal('100')
            except Exception:
                return Decimal('0.00')

        # Descuento por valor fijo
        try:
            return Decimal(str(self.descuento.valor))
        except Exception:
            return Decimal('0.00')

    @property
    def precio_final(self):
        """Calcula el precio final ya con descuento aplicado."""
        if not self.tiene_descuento:
            try:
                return Decimal(str(self.valor_producto))
            except Exception:
                return Decimal('0.00')

        try:
            vp = Decimal(str(self.valor_producto))
            precio = vp - Decimal(self.valor_descuento)
            if precio < Decimal('0.00'):
                return Decimal('0.00')
            return precio
        except Exception:
            return Decimal('0.00')

    @property
    def texto_ribbon(self):
        """Retorna el texto del listón para la UI."""
        if not self.tiene_descuento:
            return ""

        if self.descuento.tipo == "porcentaje":
            return f"-{int(self.descuento.valor)}% OFF"
        
        # Descuento por monto: formatea con separador de miles
        monto = self.descuento.valor
        try:
            monto_formateado = f"{monto:,.0f}".replace(",", ".")
        except:
            monto_formateado = str(monto)
        return f"-${monto_formateado}"
    


    class Meta:
        db_table = 'productos'
        managed  = True   

    def __str__(self):
        return self.nombre_producto
    


    
class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/')

    class Meta:
        db_table = 'imagenproducto'
        managed = False  # Si la creas tú manualmente

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    cedula = models.CharField(max_length=20, blank=True, null=True)
    fecha_registro = models.DateField(auto_now_add=True) 
    activo = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'proveedor'


class Marca(models.Model):
    nombre = models.CharField(max_length=255)
    proveedores = models.ManyToManyField(
        'Proveedor',
        blank=True,
        db_table='proveedor_marca' 
    )

    class Meta:
        db_table = 'marca' 

    def __str__(self):
        return self.nombre 
    
    


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
        
    class Meta:
        db_table = 'categoria'
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"


class Blog(models.Model):
    titulo = models.CharField(max_length=200)
    cuerpo = models.TextField()
    foto = models.ImageField(upload_to='blogs/', blank=True, null=True)

    def __str__(self):
        return self.titulo
    
    from django.db import models

class Mensaje(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=15)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Mensaje de {self.nombre}"


# ----------------
# Modelo de Stock
# ----------------
class Stock(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE, related_name='stock')
    cantidad = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'stock'

    def __str__(self):
        return f"Stock {self.producto.nombre_producto}: {self.cantidad}"


# Cuando se crea un pedido, descontar stock de los productos incluidos (si existen)
@receiver(post_save, sender=Pedido)
def decrease_stock_on_order(sender, instance, created, **kwargs):
    if not created:
        return
    productos = instance.productos or []
    for item in productos:
        if not isinstance(item, dict):
            continue
        # intentar identificar el producto por código (codigo o sku) o por nombre
        codigo = item.get('codigo') or item.get('sku')
        nombre = item.get('nombre') or item.get('name')
        try:
            cantidad = int(item.get('cantidad', item.get('qty', 1)) or 1)
        except Exception:
            cantidad = 1

        prod = None
        if codigo:
            prod = Producto.objects.filter(codigo_producto__iexact=str(codigo)).first()
        if not prod and nombre:
            prod = Producto.objects.filter(nombre_producto__iexact=nombre).first()
        if not prod:
            continue

        # Descontar de stock de forma atómica
        try:
            with transaction.atomic():
                updated = Stock.objects.filter(producto=prod, cantidad__gte=cantidad).update(cantidad=F('cantidad') - cantidad)
                if updated == 0:
                    # No había suficiente stock (o no existía registro). Ajustar a 0 si existe registro.
                    Stock.objects.filter(producto=prod).update(cantidad=0)
        except Exception:
            # No detener el procesamiento del pedido por errores de stock; registrar/loguear si es necesario
            pass


from django.db import models

class Factura(models.Model):
    invoice_id = models.CharField(max_length=100, unique=True)
    email_cliente = models.EmailField()
    producto = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50)
    creada_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.producto} - {self.estado}"

         