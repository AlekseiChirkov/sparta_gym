import json
import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
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
from shop.forms import EditProfileModelForm
from shop.services import cart_data, guest_order


def home(request):
    posts = Post.objects.order_by('date')[:3]
    user_id = request.user.id
    context = {
        'posts': posts,
        'user_id': user_id
    }
    return render(request, 'shop/home.html', context)


def train_constructor(request):
    return render(request, 'shop/train_construct.html')


@csrf_protect
def shop(request):
    user_id = request.user.id
    data = cart_data(request)
    cart_items = data['cart_items']

    products = Product.objects.all()
    product_filter = ProductFilter(request.POST, queryset=products)
    products = product_filter.qs
    context = {
        'products': products,
        'product_filter': product_filter,
        'cart_items': cart_items,
        'user_id': user_id
    }
    return render(request, 'shop/shop.html', context)


@csrf_protect
def cart(request):
    user_id = request.user.id

    data = cart_data(request)
    cart_items = data['cart_items']
    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
        'cart_items': cart_items,
        'user_id': user_id
    }
    return render(request, 'shop/cart.html', context)


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
    user_id = request.user.id
    user = request.user
    data = cart_data(request)
    cart_items = data['cart_items']
    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
        'cart_items': cart_items,
        'user_id': user_id,
        'user': user,
    }
    return render(request, 'shop/checkout.html', context)


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guest_order(request, data)

    total_str = data['form']['total']
    total_str = total_str.replace(',', '.')
    total = float(total_str)
    order.transaction_id = transaction_id
    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zip_code=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment complete!', safe=False)


@csrf_protect
@login_required(login_url='users:login')
def profile(request, id):
    user_id = request.user.id
    if request.method == 'POST':
        form = EditProfileModelForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect(f'/profile/cart/{user_id}/')
    else:
        form = EditProfileModelForm(instance=request.user.profile)

    username = request.user.username
    name = request.user.profile.name
    surname = request.user.profile.surname
    age = 0
    if request.user.profile.birthday:
        age = int(datetime.datetime.today().year) - int(request.user.profile.birthday.year)

    visited_dates = []
    subscription = []
    if request.user.is_authenticated:
        customer = request.user.customer
        try:
            subscription = Subscription.objects.get(customer=customer)
            visited_dates = subscription.visit_dates
        except Subscription.DoesNotExist:
            visited_dates = ['У вас нет действующего абонемента']

    context = {
        'username': username,
        'subscription': subscription,
        'name': name,
        'surname': surname,
        'age': age,
        'dates': visited_dates,
        'update': form,
        'user_id': user_id
    }
    return render(request, 'shop/profile.html', context)


def subscription_check(request):
    return render(request, 'shop/qrcode_post_request.html')


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (AllowAny,)

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
    permission_classes = (AllowAny,)
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = [
        'user', 'id'
    ]
    search_fields = [
        'user', 'id'
    ]
