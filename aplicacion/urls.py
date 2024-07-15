# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('tienda/', views.tienda, name='tienda'),
    path('carrito/', views.carrito, name='carrito'),
    path('registro/', views.registro, name='registro'),
    path('pagar/', views.pagar_view, name='pagar'),
    path('eliminar-del-carrito/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('actualizar-cantidad/<int:item_id>/', views.actualizar_cantidad, name='actualizar_cantidad'),
    path('agregar-al-carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('confirmacion/<int:orden_id>/', views.confirmacion_pago_view, name='confirmacion_pago'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('accounts/login/', views.login_view, name='login'),
    path('logout/', exit, name='exit'),
    
]
