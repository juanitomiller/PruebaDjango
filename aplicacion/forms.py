from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from aplicacion.models import Producto
from .models import UserProfile
from django.utils.translation import gettext_lazy as _


class UserProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label=_('Fecha de nacimiento')
    )

    class Meta:
        model = UserProfile
        fields = ['date_of_birth']


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label=_('Correo electrónico'))
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label=_('Fecha de nacimiento')
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'date_of_birth', 'password1', 'password2']
        labels = {
            'username': _('Nombre de usuario'),
            'first_name': _('Nombre'),
            'last_name': _('Apellido'),
            'password1': _('Contraseña'),
            'password2': _('Confirmar contraseña'),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Este correo electrónico ya está registrado'))
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            user_profile = UserProfile(user=user, date_of_birth=self.cleaned_data['date_of_birth'])
            user_profile.save()
        return user


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'imagen']
        labels = {
            'nombre': _('Nombre'),
            'descripcion': _('Descripción'),
            'precio': _('Precio'),
            'stock': _('Stock'),
            'imagen': _('Imagen'),
        }
