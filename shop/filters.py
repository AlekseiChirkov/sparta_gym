import django_filters
from django import forms

from shop.models import Product, ProductType


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        label='search',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder': 'ЧТО ИЩЕМ? (Название продукта)'})
    )
    product_type = django_filters.ModelChoiceFilter(
        queryset=ProductType.objects.all(),
        empty_label='ТОВАР ПО КАТЕГОРИЯМ',
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )

    class Meta:
        model = Product
        exclude = ['image']

