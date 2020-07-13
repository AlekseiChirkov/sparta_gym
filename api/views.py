from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_protect
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from rest_auth.registration.views import RegisterView

from .tokens import account_activation_token
from .forms import *


def home(request):
    posts = Post.objects.order_by('date')[:3]
    return render(request, 'api/home.html', {'posts': posts})


def signup_form(request):
    if request.method == 'POST':
        signup = UserCreationForm(request.POST)

        if signup.is_valid():
            user = signup.save(commit=False)
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
            to_email = signup.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Пожалуйста, подтвердите ваш email, чтобы завершить регистрацию.')
    else:
        signup = UserCreationForm()
    return render(request, 'api/registration.html', {'signup': signup})


@csrf_protect
def login_form(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.info(request, "Username or password is incorrect.")

    context = {}
    return render(request, 'api/login.html', context)


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


def shop(request):
    products = Product.objects.order_by('date')
    context = {'products': products}
    return render(request, 'api/shop.html', context)


def profile(request):
    context = {}
    return render(request, 'api/profile.html', context)
