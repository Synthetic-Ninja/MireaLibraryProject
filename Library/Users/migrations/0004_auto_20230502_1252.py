# Generated by Django 3.2.18 on 2023-05-02 12:52

import Users.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_auto_20230502_1208'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterField(
            model_name='user',
            name='basket',
            field=models.JSONField(default=Users.models.default_basket, verbose_name='Корзина'),
        ),
        migrations.AlterField(
            model_name='user',
            name='document_number',
            field=models.CharField(default='', max_length=50, validators=[django.core.validators.RegexValidator(code='invalid_document_number', message='Неверный номер документа', regex='^\\d{6}$')], verbose_name='Номер документа'),
        ),
        migrations.AlterField(
            model_name='user',
            name='document_seria',
            field=models.CharField(default='', max_length=50, validators=[django.core.validators.RegexValidator(code='invalid_document_seria', message='Неверная серия документа', regex='^((\\d+-[А-Яа-я]{2})|(\\d{4}))$')], verbose_name='Серия документа'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Электронная почта'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(upload_to='books_images', verbose_name='Аватар'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128, verbose_name='Пароль'),
        ),
    ]