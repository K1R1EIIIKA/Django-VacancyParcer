from django.forms import TextInput, ModelForm, NumberInput

from .models import *


class CreateCall(ModelForm):
    class Meta:
        model = ApiCall

        fields = ['city', 'vacancy', 'count']

        widgets = {
            'city': TextInput(attrs={
                'class': 'form-account-control',
                'name': 'city',
                'placeholder': 'Город'
            }),
            'vacancy': TextInput(attrs={
                'class': 'form-account-control',
                'name': 'vacancy',
                'placeholder': 'Вакансия'
            }),
            'count': NumberInput(attrs={
                'class': 'form-account-control',
                'name': 'count',
                'placeholder': 'Количество'
            }),
        }
