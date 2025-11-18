from django import forms
from .models import Producto



class RegistroForm(forms.Form):
    nombre = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'Nombre'}))
    correo = forms.EmailField(max_length=255, required=True, widget=forms.EmailInput(attrs={'placeholder': 'Correo Electrónico'}))
    contraseña = forms.CharField(max_length=255, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))
    confirmar_contraseña = forms.CharField(max_length=255, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar Contraseña'}))

    def clean(self):
        cleaned_data = super().clean()
        contraseña = cleaned_data.get('contraseña')
        confirmar = cleaned_data.get('confirmar_contraseña')

        if contraseña and confirmar and contraseña != confirmar:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        
        return cleaned_data




# core/forms.py
from django import forms
from .models import Descuento, Producto

class DescuentoForm(forms.ModelForm):
    class Meta:
        model = Descuento
        fields = [
            'codigo', 'nombre', 'descripcion', 'tipo', 'valor',
            'max_uso', 'aplicable_a', 'fecha_inicio', 'fecha_fin',
            'activo', 'observaciones'
        ]
        widgets = {
            'fecha_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'fecha_fin': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }






from django import forms
from .models import Producto, Categoria, Proveedor, Marca, Stock

class ProductoForm(forms.ModelForm):
    stock_cantidad = forms.IntegerField(required=False, min_value=0, initial=0, label='Stock',
                                       widget=forms.NumberInput(attrs={'placeholder': 'Stock', 'min': '0', 'class':'form-control'}))

    class Meta:
        model = Producto
        fields = [
            'codigo_producto',
            'nombre_producto',
            'descripcion_producto',
            'valor_producto',
            'categoria',
            'marca',
            'proveedor',
            'imagen_producto',
            'tallas_disponibles',
            'colores_disponibles',
            'descuento',    # <- agregado
        ]
        widgets = {
            'codigo_producto': forms.TextInput(attrs={'class':'form-control','placeholder':'Código del Producto'}),
            'nombre_producto': forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre del Producto'}),
            'descripcion_producto': forms.Textarea(attrs={'class':'form-control','rows':3,'placeholder':'Descripción'}),
            'valor_producto': forms.NumberInput(attrs={'class':'form-control','step':'0.01'}),
            'categoria': forms.Select(attrs={'class':'form-select'}),
            'marca': forms.Select(attrs={'class':'form-select'}),
            'proveedor': forms.Select(attrs={'class':'form-select'}),
            'imagen_producto': forms.ClearableFileInput(attrs={'class':'form-control'}),
            'tallas_disponibles': forms.TextInput(attrs={'class':'form-control'}),
            'colores_disponibles': forms.TextInput(attrs={'class':'form-control'}),
            'descuento': forms.Select(attrs={'class':'form-select'}),  # widget para descuento
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # placeholders y clases
        if 'codigo_producto' in self.fields:
            self.fields['codigo_producto'].widget.attrs.update({'placeholder': 'Código del Producto'})
        if 'nombre_producto' in self.fields:
            self.fields['nombre_producto'].widget.attrs.update({'placeholder': 'Nombre del Producto'})
        if 'descripcion_producto' in self.fields:
            self.fields['descripcion_producto'].widget.attrs.update({'placeholder': 'Descripción'})

        # Querysets para selects
        if 'marca' in self.fields:
            self.fields['marca'].queryset = Marca.objects.all()
            self.fields['marca'].empty_label = 'Seleccionar marca'
        if 'proveedor' in self.fields:
            self.fields['proveedor'].queryset = Proveedor.objects.all()
            self.fields['proveedor'].empty_label = 'Seleccionar proveedor'
        if 'categoria' in self.fields:
            self.fields['categoria'].queryset = Categoria.objects.all()
            self.fields['categoria'].empty_label = 'Seleccionar categoría'

        # Descuentos: mostrar solo activos y/o vigentes (ajusta filtro si quieres otra lógica)
        if 'descuento' in self.fields:
            # puedes filtrar por activo y vigencia si tu modelo Descuento tiene esos campos
            try:
                self.fields['descuento'].queryset = Descuento.objects.filter(activo=True)
            except Exception:
                # fallback si aún no existe la tabla/descuento
                self.fields['descuento'].queryset = Descuento.objects.all()
            self.fields['descuento'].required = False
            self.fields['descuento'].empty_label = 'Sin descuento'

        # inicializar stock si la instancia tiene stock
        if 'stock_cantidad' in self.fields:
            try:
                if getattr(self, 'instance', None) and hasattr(self.instance, 'stock') and self.instance.stock is not None:
                    self.fields['stock_cantidad'].initial = self.instance.stock.cantidad
            except Exception:
                pass

    def save(self, commit=True):
        producto = super().save(commit=commit)
        # sincronizar tabla Stock si la usas
        try:
            stock_val = self.cleaned_data.get('stock_cantidad')
        except Exception:
            stock_val = None
        if commit and stock_val is not None:
            try:
                Stock.objects.update_or_create(producto=producto, defaults={'cantidad': int(stock_val)})
            except Exception:
                pass
        else:
            if stock_val is not None:
                setattr(producto, '_pending_stock', stock_val)
        return producto
from .models import Categoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la categoría'}),
        }

from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'correo', 'rol']

from django import forms
from .models import Marca, Proveedor

class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nombre', 'proveedores']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la marca'}),
            'proveedores': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        
from .models import Proveedor

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'correo', 'telefono', 'cedula', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

from .models import Blog, Mensaje

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['titulo', 'cuerpo', 'foto']
        
from django import forms
from .models import Mensaje

class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['nombre', 'correo', 'telefono', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su correo'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su número'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese su mensaje', 'rows': 4}),
        }




