import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


def default_basket() -> dict:
    return {'items': []}


class User(AbstractUser):
    first_name = models.CharField(max_length=150, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=150, blank=True, verbose_name='Фамилия')
    password = models.CharField(max_length=128, verbose_name='Пароль')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='books_images', verbose_name='Аватар')
    email = models.EmailField(unique=True, blank=False, verbose_name='email')
    cart = models.JSONField(default=default_basket, verbose_name='Корзина')
    document_seria = models.CharField(max_length=50,
                                      default='',
                                      validators=[RegexValidator(regex=r'^((\d+-[А-Яа-я]{2})|(\d{4}))$',
                                                                 message='Неверная серия документа',
                                                                 code='invalid_document_seria')],
                                      verbose_name='Серия документа')

    document_number = models.CharField(max_length=50,
                                       default='',
                                       validators=[RegexValidator(regex=r'^\d{6}$',
                                                                  message='Неверный номер документа',
                                                                  code='invalid_document_number')],
                                       verbose_name='Номер документа')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def clean(self):
        super().clean()
        if User.objects.filter(document_seria=self.document_seria, document_number=self.document_number):
            raise ValidationError("Пользователь с таким документом уже существует")
    
