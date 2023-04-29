from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import *
from main.models import *


def account(request):
    error = ''

    if request.user.is_authenticated:
        form = UserInfoForm(data=request.POST)

        if request.method == 'POST':
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user

                if UserInfo.objects.filter(user=post.user).exists():
                    UserInfo.objects.filter(user=post.user).update(email=post.email, telegram=post.telegram)
                else:
                    post.save()

                return redirect('account_home')
            else:
                error = 'Неправильно введенные данные'
        else:
            form = UserInfoForm(instance=UserInfo.objects.get(user=request.user))

        calls = ApiCall.objects.filter(user=request.user).order_by('-id')
        hhru_vacancies = HhruVacancyList.objects.filter(user=request.user)
        superjob_vacancies = SuperjobVacancyList.objects.filter(user=request.user)
        zarplataru_vacancies = ZarplataruVacancyList.objects.filter(user=request.user)

        data = {
            'calls': calls,
            'hhru_vacancies': hhru_vacancies,
            'superjob_vacancies': superjob_vacancies,
            'zarplataru_vacancies': zarplataru_vacancies,
            'form': form,
            'error': error,
        }

        return render(request, 'account/account.html', data)
    else:
        return redirect('login')


def register(request):
    if request.user.is_authenticated:
        return redirect('account_home')
    else:
        error = ''
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)

            if form.is_valid():
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(username=username, password=password)

                login(request, user)
                UserInfo.objects.create(user=user, email=user.email)
                return redirect('home')
            else:
                error = 'Неправильно введенные данные'

        data = {
            'form': form,
            'error': error
        }
        return render(request, 'registration/register.html', data)


def login_acc(request):
    if request.user.is_authenticated:
        return redirect('account_home')
    else:
        error = ''
        form = Authenticate()

        if request.method == 'POST':
            form = Authenticate(data=request.POST)

            if form.is_valid():
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(username=username, password=password)

                if user is not None:
                    login(request, user)
                    return redirect('account_home')
            else:
                error = 'Неправильно введенные данные'
        data = {
            'form': form,
            'error': error,
        }
    return render(request, 'registration/login.html', data)


@login_required(login_url='login')
def logout_acc(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('home')
