from django.db import models
from django.contrib.auth.models import User


class ApiCall(models.Model):
    vacancy = models.CharField('Вакансия', max_length=50)
    city = models.CharField('Город', max_length=50)
    count = models.IntegerField('Количество вакансий')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.count) + ' ' + self.user.username + ' ' + self.vacancy + ' ' + self.city


class HhruVacancyList(models.Model):
    vacancy = models.CharField('Вакансия', max_length=50)
    city = models.CharField('Город', max_length=50)
    data = models.JSONField('JSON', default=dict)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    call = models.ForeignKey(ApiCall, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' ' + self.vacancy + ' ' + self.city


class SuperjobVacancyList(models.Model):
    vacancy = models.CharField('Вакансия', max_length=50)
    city = models.CharField('Город', max_length=50)
    data = models.JSONField('JSON', default=dict)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    call = models.ForeignKey(ApiCall, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' ' + self.vacancy + ' ' + self.city


class ZarplataruVacancyList(models.Model):
    vacancy = models.CharField('Вакансия', max_length=50)
    city = models.CharField('Город', max_length=50)
    data = models.JSONField('JSON', default=dict)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    call = models.ForeignKey(ApiCall, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' ' + self.vacancy + ' ' + self.city
