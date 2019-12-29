from django.http import Http404
from django.shortcuts import render
from django.contrib import messages
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from rest_auth.registration.views import RegisterView

from .serializers import *
from .forms import *


def home(request):
    posts = Post.objects.all().order_by('date')
    return render(request, 'api/home.html', {'posts': posts})


def registration(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        print(request.POST)
        print(form.cleaned_data)
        data = form.cleaned_data
        new_form = form.save()
        messages.success(request, 'Администрация SpartA Gym благодарит вас за регистрацию!')
    return render(request, 'api/registration.html', locals())

def train_constructor(request):
    return render(request, 'api/train_construct.html')

class SubscriptionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def get(self, request):
        subscription = self.queryset.all()
        serializer = self.serializer_class(subscription, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        pk = request.data.get('id', None)
        if pk is None:
            raise ParseError('id is required')

        try:
            subscriptions = self.queryset.get(id=pk)
        except Subscription.DoesNotExist:
            raise Http404
        else:
            subscriptions.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class ProductTypeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = ProductType.objects.all()
    serializer_class = ProductTypesSerializer

    def get(self, request):
        product = self.queryset.all()
        serializer = self.serializer_class(product, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        pk = request.data.get('id', None)
        if pk is None:
            raise ParseError('id is required')

        try:
            product = self.queryset.get(id=pk)
        except ProductType.DoesNotExist:
            raise Http404
        else:
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request):
        product = self.queryset.all()
        serializer = self.serializer_class(product, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        pk = request.data.get('id', None)
        if pk is None:
            raise ParseError('id is required')

        try:
            product = self.queryset.get(id=pk)
        except Product.DoesNotExist:
            raise Http404
        else:
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class CustomRegisterView(RegisterView):
    queryset = MyUser.objects.all()
    serializer_class = CustomUserDetailsSerializer

    def get(self, request):
        user = self.queryset.all()
        serializer = self.serializer_class(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        pk = request.data.get()
        if pk is None:
            raise ParseError('id is required')

        try:
            user = self.queryset.get(id=pk)
        except MyUser.DoesNotExist:
            raise Http404
        else:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class UsersSubscriptionsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer

    def get(self, request):
        user_subscription = self.queryset.all()
        serializer = self.serializer_class(user_subscription, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        pk = request.data.get()
        if pk is None:
            raise ParseError('id is required')

        try:
            user_subscription = self.queryset.get(id=pk)
        except UserSubscription.DoesNotExist:
            raise Http404
        else:
            user_subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class PaymentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get(self, request):
        payment = self.queryset.all()
        serializer = self.serializer_class(payment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        pk = request.data.get()
        if pk is None:
            raise ParseError('id is required')

        try:
            payment = self.queryset.get(id=pk)
        except Payment.DoesNotExist:
            raise Http404
        else:
            payment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class PaymentProductViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = PaymentProduct.objects.all()
    serializer_class = PaymentProductSerializer

    def get(self, request):
        payment = self.queryset.all()
        serializer = self.serializer_class(payment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        pk = request.data.get()
        if pk is None:
            raise ParseError('id is required')

        try:
            payment = self.queryset.get(id=pk)
        except PaymentProduct.DoesNotExist:
            raise Http404
        else:
            payment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request):
        post = self.queryset.all()
        serializer = self.serializer_class(post, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        pk = request.data.get()
        if pk is None:
            raise ParseError('id is required')

        try:
            post = self.queryset.get(id=pk)
        except Post.DoesNotExist:
            raise Http404
        else:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
