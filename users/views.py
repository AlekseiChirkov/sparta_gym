import datetime

from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import login, authenticate
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site

from .tokens import account_activation_token
from .forms import *


@csrf_protect
def signup_form(request):
    if request.method == 'POST':
        signup = UserCreationForm(request.POST)

        if signup.is_valid():
            user = signup.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Активация аккаунта SpartA GYM'
            message = render_to_string('shop/acc_active_email.html', {
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
    return render(request, 'shop/registration.html', {'signup': signup})


@csrf_protect
def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('users:profile')
        else:
            message = "Неверный логин или пароль."
            return render(request, 'shop/login.html', {'message': message})

    context = {}
    return render(request, 'shop/login.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('users:login')
    else:
        return HttpResponse('Ссылка не действительна!')


@csrf_protect
@login_required(login_url='users:login')
def profile(request):
    username = request.user.username
    name = request.user.profile.name
    surname = request.user.profile.surname
    age = 0
    if request.user.profile.birthday:
        age = int(datetime.datetime.today().year) - int(request.user.profile.birthday.year)
    context = {
        'username': username,
        'name': name,
        'surname': surname,
        'age': age,
    }
    return render(request, 'shop/templates/shop/profile.html', context)
