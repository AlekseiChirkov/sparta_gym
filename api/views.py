from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from rest_auth.registration.views import RegisterView

from .serializers import *
from .forms import *


def home(request):
    posts = Post.objects.order_by('date')[:3]
    return render(request, 'api/home.html', {'posts': posts})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Активация аккаунта SpartA GYM'
            message = render_to_string('api/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Пожалуйста, подтвердите ваш email, чтобы завершить регистрацию.')
    else:
        form = UserCreationForm()
    return render(request, 'api/registration.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Спасибо за подтверждение. Теперь вы можете войти в личный кабинет')
    else:
        return HttpResponse('Ссылка не действительна!')


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
