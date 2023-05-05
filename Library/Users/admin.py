from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ValidationError

from .models import User
from django import forms

from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):

    username = forms.CharField(widget=forms.TextInput, label='Имя пользователя')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Подтверждение пароля')

    class Meta:
        model = UserCreationForm.Meta.model
        fields = '__all__'
        field_classes = UserCreationForm.Meta.field_classes


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    add_fieldsets = (
        ('Данные для входа', {'fields': ('username', 'password1', 'password2')}),
        ('Персональные данные', {'fields': ('first_name', 'last_name', 'email', 'document_seria', 'document_number')}),
    )

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'document_seria', 'document_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
    )
