from django.urls import path

from .views import UserLoginView, UserRegistrationView, UserProfileView, add_to_cart, drop_from_cart
from django.contrib.auth.views import LogoutView

app_name = 'Users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('add_to_cart/<int:book_id>/', add_to_cart, name='add_to_cart'),
    path('drop_from_cart/<int:book_id>/', drop_from_cart, name='drop_from_cart')
]