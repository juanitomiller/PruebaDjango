from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, ProductoForm
from django.contrib.auth.forms import AuthenticationForm
from .models import OrdenDePago, Producto
from django.contrib.auth.decorators import login_required
import logging
from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

# views.py
from django.shortcuts import render
from .models import Producto

def index(request):
    return render(request, 'aplicacion/index.html')

def nosotros(request):
    active_urls = ['perfumeria_femenina', 'perfumeria_femenina_detalle', 'perfumeria_masculina', 'perfumeria_masculina_detalle']
    return render(request, 'aplicacion/nosotros.html', {'active_urls': active_urls})

@login_required
def tienda(request):
    productos_femeninos = Producto.objects.filter(sexo='Femenino')
    productos_masculinos = Producto.objects.filter(sexo='Masculino')
    return render(request, 'aplicacion/tienda.html', {
        'productos_femeninos': productos_femeninos,
        'productos_masculinos': productos_masculinos
    })

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

def perfumeria_femenina(request):
    # lógica de la vista
    return render(request, 'aplicacion/perfumeria_femenina.html')

def perfumeria_masculina(request):
    # lógica de la vista
    return render(request, 'aplicacion/masculina.html')            

@login_required
def pagar_view(request):
    if request.method == 'POST':
        productos_carrito = request.session.get('cart', [])
        total = sum(producto['price'] * producto['quantity'] for producto in productos_carrito)

        orden = OrdenDePago.objects.create(
            usuario=request.user,
            total=total,
            estado='pendiente'
        )

        return redirect('confirmacion_pago', orden_id=orden.id)

    return render(request, 'aplicacion/pagar.html')

@login_required
def confirmacion_pago_view(request, orden_id):
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
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def exit(request):
    logout(request)
    return redirect('index')


#CARRITO:


@login_required
def carrito(request):
    cart = request.session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    context = {
        'carrito_items': cart.values(),
        'total': total
    }
    return render(request, 'aplicacion/carrito.html', context)

@login_required
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('tienda')
    else:
        form = ProductoForm()
    return render(request, 'aplicacion/producto_agregar.html', {'form': form})


@login_required
def eliminar_del_carrito(request, producto_id):
    cart = request.session.get('cart', {})
    if str(producto_id) in cart:
        del cart[str(producto_id)]
        request.session['cart'] = cart
    return redirect('carrito')


@login_required
def editar_producto(request, producto_id):
    producto = Producto.objects.get(pk=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('tienda')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'aplicacion/producto_editar.html', {'form': form, 'producto': producto})


@login_required
def vaciar_carrito(request):
    try:
        # Eliminar todos los productos del carrito en la sesión
        request.session['cart'] = {}
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})



# Métodos AJAX para manejar el carrito

@csrf_exempt
@require_POST
@login_required
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product = get_object_or_404(Producto, id=product_id)
    
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {
            'name': product.nombre,
            'price': float(product.precio),  # Convertimos Decimal a float
            'quantity': 1
        }
    
    request.session['cart'] = cart
    return JsonResponse({'success': True})


@csrf_exempt
@require_POST
@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    
    carrito_items = [
        {'id': key, 'name': value['name'], 'price': value['price'], 'quantity': value['quantity']} 
        for key, value in cart.items()
    ]
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return JsonResponse({'success': True, 'carrito_items': carrito_items, 'total': total})

@csrf_exempt
@require_POST
@login_required
def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
        request.session['cart'] = cart
        return JsonResponse({'success': True, 'quantity': cart[str(product_id)]['quantity']})
    return JsonResponse({'success': False})


@csrf_exempt
@require_POST
@login_required
def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        if cart[str(product_id)]['quantity'] > 1:
            cart[str(product_id)]['quantity'] -= 1
        else:
            del cart[str(product_id)]
        request.session['cart'] = cart
        return JsonResponse({'success': True, 'quantity': cart.get(str(product_id), {}).get('quantity', 0)})
    return JsonResponse({'success': False})

@login_required
def get_cart(request):
    cart = request.session.get('cart', {})
    carrito_items = [
        {'id': key, 'name': value['name'], 'price': value['price'], 'quantity': value['quantity']} 
        for key, value in cart.items()
    ]
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return JsonResponse({'carrito_items': carrito_items, 'total': total})


@login_required
def get_cart_count(request):
    cart = request.session.get('cart', {})
    cart_count = len(cart)
    return JsonResponse({'cart_count': cart_count})




