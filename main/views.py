from django.shortcuts import render

from .forms import *
from .models import *
from account.models import *
from main.services.parser import *
from main.management.commands.bot import send_message_to_user


def index(request):
    error = ''
    form = CreateCall(data=request.POST)

    if request.method == 'POST':
        # print(request.POST)
        data = {
            'form': form,

            'error': error,
        }

        if 'parce' in request.POST:
            if form.is_valid():
                post = form.save(commit=False)
                if request.user.is_authenticated:
                    post.user = request.user
                    post.save()
                else:
                    post.user = User.objects.get(id=1)
                    post.save()

                # form = CreateCall()

                hhru_vacancies = HhruVacancyList.objects.create(
                    vacancy=post.vacancy,
                    city=post.city,
                    user=post.user,
                    call=post,
                    data=get_hhru_vacancies(post.vacancy, post.city, post.count))

                superjob_vacancies = SuperjobVacancyList.objects.create(
                    vacancy=post.vacancy,
                    city=post.city,
                    user=post.user,
                    call=post,
                    data=get_superjob_vacancies(post.vacancy, post.city, post.count))

                zarplataru_vacancies = ZarplataruVacancyList.objects.create(
                    vacancy=post.vacancy,
                    city=post.city,
                    user=post.user,
                    call=post,
                    data=get_zarplataru_vacancies(post.vacancy, post.city, post.count))

                data['hhru_vacancies'] = hhru_vacancies
                data['superjob_vacancies'] = superjob_vacancies
                data['zarplataru_vacancies'] = zarplataru_vacancies

            return render(request, 'main/index.html', data)

        if 'send_to_telegram' in request.POST and request.user.is_authenticated:
            # last HhruVacancyList from user
            hhru_vacancies = HhruVacancyList.objects.filter(user=request.user).last()
            hhru_vacancies.data = get_hhru_vacancies(hhru_vacancies.vacancy, hhru_vacancies.city,
                                                     hhru_vacancies.call.count)
            data['hhru_vacancies'] = hhru_vacancies

            superjob_vacancies = SuperjobVacancyList.objects.filter(user=request.user).last()
            superjob_vacancies.data = get_superjob_vacancies(superjob_vacancies.vacancy, superjob_vacancies.city,
                                                             superjob_vacancies.call.count)
            data['superjob_vacancies'] = superjob_vacancies

            zarplataru_vacancies = ZarplataruVacancyList.objects.filter(user=request.user).last()
            zarplataru_vacancies.data = get_zarplataru_vacancies(zarplataru_vacancies.vacancy,
                                                                 zarplataru_vacancies.city,
                                                                 zarplataru_vacancies.call.count)
            data['zarplataru_vacancies'] = zarplataru_vacancies

            send_message_to_user(UserInfo.objects.get(user=request.user).telegram,
                                 request.POST['vacancy'],
                                 request.POST['city'],
                                 hhru_vacancies.data,
                                 superjob_vacancies.data,
                                 zarplataru_vacancies.data)

            return render(request, 'main/index.html', data)

    data = {
        'form': form,
        'error': error,
    }

    return render(request, 'main/index.html', data)
