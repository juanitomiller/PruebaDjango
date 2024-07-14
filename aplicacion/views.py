from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import  AuthenticationForm
from .models import OrdenDePago, Producto, ItemCarrito
from django.contrib.auth.decorators import login_required
import logging
from django.http import JsonResponse


# views.py
from django.shortcuts import render
from .models import Producto

def index(request):
    return render(request, 'aplicacion/index.html')

def nosotros(request):
    return render(request, 'aplicacion/nosotros.html')

@login_required
def tienda(request):
    productos = Producto.objects.all()
    return render(request, 'aplicacion/tienda.html', {'productos': productos})


def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('tienda')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'aplicacion/registro.html', {'form': form})

@login_required
def pagar_view(request):
    # Lógica de la vista de pago
    if request.method == 'POST':
        # Recibir los datos del formulario (ejemplo)
        productos_carrito = request.session.get('carrito', [])  # Obtener productos del carrito de la sesión

        # Calcular el total de la compra
        total = sum(producto['precio'] * producto['cantidad'] for producto in productos_carrito)

        # Crear una nueva orden de pago
        orden = OrdenDePago.objects.create(
            usuario=request.user,  # Ajusta según cómo manejas la autenticación de usuarios
            total=total,
            estado='pendiente'  # Puedes establecer un estado inicial como pendiente
        )

        # Ejemplo: Redirigir a una página de confirmación de pago
        return redirect('confirmacion_pago', orden_id=orden.id)  # Ajusta según tu configuración de URLs

    # Renderizar el template de pago
    return render(request, 'aplicacion/pagar.html')

@login_required
def confirmacion_pago_view(request, orden_id):
    # Lógica para obtener la orden de pago y mostrar la confirmación de pago
    return render(request, 'confirmacion_pago.html', {'orden_id': orden_id})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index') 
            else:
                pass
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def exit(request):
    logout(request)
    return redirect('index')


#CARRITO:

@login_required
def carrito(request):
    carrito_items = ItemCarrito.objects.filter(usuario=request.user)
    total = sum(item.producto.precio * item.cantidad for item in carrito_items)
    return render(request, 'aplicacion/carrito.html', {'carrito_items': carrito_items, 'total': total})

logger = logging.getLogger(__name__)

@login_required
def agregar_al_carrito(request, producto_id):
    if request.method == 'POST':
        try:
            producto = get_object_or_404(Producto, id=producto_id)
            # Aquí va la lógica para agregar el producto al carrito
            logger.debug(f'Producto agregado al carrito: {producto.nombre}')
            return JsonResponse({'mensaje': 'Producto agregado al carrito correctamente.'})
        except Exception as e:
            logger.error(f'Error al agregar producto al carrito: {e}')
            return JsonResponse({'error': 'Hubo un problema al agregar el producto al carrito. Inténtelo de nuevo más tarde.'}, status=500)

def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, pk=item_id)
    producto_nombre = item.producto.nombre
    item.delete()
    messages.success(request, f"{producto_nombre} fue eliminado del carrito.")
    return redirect('carrito')

def actualizar_cantidad(request, item_id):
    item = get_object_or_404(ItemCarrito, pk=item_id)
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad'))
        if cantidad > 0:
            item.cantidad = cantidad
            item.save()
            messages.success(request, "Cantidad actualizada.")
        else:
            item.delete()
            messages.success(request, "Producto eliminado del carrito.")
    return redirect('carrito')