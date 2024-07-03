# forms.py
from django import forms

from .models import Product, Comment, Order


class ProductForm(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    price = forms.FloatField()
    rating = forms.FloatField()
    discount = forms.IntegerField()
    quantity = forms.IntegerField()


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'slug', 'description', 'price', 'discount', 'image', 'rating', 'on_sale')


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('name', 'email', 'quantity')


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
