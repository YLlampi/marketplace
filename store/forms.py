from PIL import Image
from django import forms
from django.core.exceptions import ValidationError

from .models import Product, Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'address', 'zipcode', 'city',)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'title', 'description', 'price', 'quantity', 'image', 'image_two', 'image_three', 'departamento', 'status')

        widgets = {
            'category': forms.Select(attrs={
                'class': 'w-full p-4 border border-gray-200'
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full p-4 border border-gray-200'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-4 border border-gray-200'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full p-4 border border-gray-200'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'w-full p-4 border border-gray-200'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full p-4 border border-gray-200'
            }),
            'image_two': forms.FileInput(attrs={
                'class': 'w-full p-4 border border-gray-200'
            }),
            'image_three': forms.FileInput(attrs={
                'class': 'w-full p-4 border border-gray-200'
            }),
        }
