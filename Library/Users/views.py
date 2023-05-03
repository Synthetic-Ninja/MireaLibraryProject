from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from common.views import TitleMixin

from .forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from .models import User
from Books.models import Book


class UserLoginView(TitleMixin, LoginView):
    template_name = 'Users/login.html'
    title = 'Book Heaven - Авторизация'
    form_class = UserLoginForm


class UserRegistrationView(TitleMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'Users/register.html'
    title = 'Book Heaven - Регистрация'
    success_url = reverse_lazy('Users:login')


class UserProfileView(LoginRequiredMixin, TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'Users/profile.html'
    title = 'Book Heaven - Профиль'
    # Строка нужная для LoginRequiredMixin, которая служит для перенаправления пользователя,
    # если он не залогинен
    login_url = reverse_lazy('Users:login')
    success_url = reverse_lazy('Users:profile')
    # Переопределенный метод родителя SingleObjectMixin

    def get_object(self, queryset=None):
        user = self.get_queryset().get(pk=self.request.user.id)
        return user

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['cart'] = Book.objects.all().filter(id__in=data.get('user').cart['items'])
        return data


@login_required
def add_to_cart(request, book_id):
    user = User.objects.get(id=request.user.id)
    user_cart = user.cart['items']
    if book_id not in user_cart:
        user.cart['items'] = user_cart + [book_id]
        user.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def drop_from_cart(request, book_id):
    user = User.objects.get(id=request.user.id)
    user.cart['items'].remove(book_id)
    user.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
