import json
import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from shop.filters import ProductFilter
from shop.models import *
from shop.serializers import SubscriptionSerializer


def home(request):
    posts = Post.objects.order_by('date')[:3]
    return render(request, 'shop/home.html', {'posts': posts})


def train_constructor(request):
    return render(request, 'shop/train_construct.html')


@csrf_protect
def shop(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cart_items = order['get_cart_items']

    products = Product.objects.all()
    product_filter = ProductFilter(request.POST, queryset=products)
    products = product_filter.qs
    context = {
        'products': products,
        'product_filter': product_filter,
        'cart_items': cart_items,
    }
    return render(request, 'shop/shop.html', context)


@csrf_protect
@login_required(login_url='users:login')
def cart(request):
    username = request.user.username
    name = request.user.profile.name
    surname = request.user.profile.surname
    age = 0
    if request.user.profile.birthday:
        age = int(datetime.datetime.today().year) - int(request.user.profile.birthday.year)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
        visited_dates = []
        try:
            subscription = Subscription.objects.get(customer=customer)
            visited_dates = subscription.visit_dates
        except Subscription.DoesNotExist:
            visited_dates = ['У вас нет действующего абонемента']
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cart_items = order['get_cart_items']
        visited_dates = 'У вас нет абонемента.'

    context = {
        'username': username,
        'name': name,
        'surname': surname,
        'age': age,
        'items': items,
        'order': order,
        'cart_items': cart_items,
        'dates': visited_dates
    }
    return render(request, 'shop/profile.html', context)


def update_item(request):
    data = json.loads(request.body)

    product_id = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=product_id)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        order_item.quantity = (order_item.quantity + 1)
    elif action == 'remove':
        order_item.quantity = (order_item.quantity - 1)

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('Item was added', safe=False)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cart_items = order['get_cart_items']

    context = {
        'items': items,
        'order': order,
        'cart_items': cart_items
    }
    return render(request, 'shop/checkout.html', context)


def subscription_check(request):
    return render(request, 'shop/qrcode_post_request.html')


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (AllowAny, )

    def list(self, request, *args, **kwargs):
        sub = self.queryset.all()
        serializer = self.serializer_class(sub, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(request=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class SubscriptionSearchListAPIView(ListAPIView):
    permission_classes = (AllowAny, )
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = [
        'user', 'id'
    ]
    search_fields = [
        'user', 'id'
    ]
