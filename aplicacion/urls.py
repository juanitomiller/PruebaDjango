from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('tienda/', views.tienda, name='tienda'),
    path('registro/', views.registro, name='registro'),
    path('pagar/', views.pagar_view, name='pagar'),
    path('confirmacion_pago/<int:orden_id>/', views.confirmacion_pago_view, name='confirmacion_pago'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.exit, name='logout'),
    path('carrito/', views.carrito, name='carrito'),
    path('agregar_producto/', views.agregar_producto, name='agregar_producto'),
    path('eliminar_del_carrito/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('editar_producto/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('get-cart-count/', views.get_cart_count, name='get_cart_count'),
    path('get-cart/', views.get_cart, name='get_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase-quantity/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease-quantity/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('vaciar-carrito/', views.vaciar_carrito, name='vaciar_carrito'),
    path('perfumeria_femenina/', views.perfumeria_femenina, name='perfumeria_femenina'),
    path('perfumeria_masculina/', views.perfumeria_femenina, name='perfumeria_masculina'),
    
]
