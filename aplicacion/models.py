from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)  # Asegúrate de que el campo stock esté definido si lo necesitas
    imagen = models.ImageField(upload_to='productos/')
    sexo = models.CharField(max_length=10, choices=[('Femenino', 'Femenino'), ('Masculino', 'Masculino'), ('Unisex', 'Unisex')], default='Unisex')
    fecha_creacion = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.nombre
    

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.producto.nombre} - {self.cantidad}'


class OrdenDePago(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username