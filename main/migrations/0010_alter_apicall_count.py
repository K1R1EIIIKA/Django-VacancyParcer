# Generated by Django 4.1.7 on 2023-04-21 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_apicall_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apicall',
            name='count',
            field=models.IntegerField(verbose_name='Количество вакансий'),
        ),
    ]
