from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http import Http404
from django.views.generic import ListView
from common.views import TitleMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .models import Order
from Books.models import Book


class OrdersListView(TitleMixin, LoginRequiredMixin, ListView):
    model = Order
    title = 'Book Heaven - Orders'
    template_name = 'Orders/orders.html'
    login_url = reverse_lazy('Users:login')
    success_url = reverse_lazy('Users:profile')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user__id=self.request.user.id).order_by('-id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if objects := context['object_list']:
            context['overdue_objects'] = objects.filter(status='overdue')
        return context


@login_required
def create_orders(request):
    if not (items := request.user.cart['items']):
        raise Http404
    success_orders = []
    error_orders = []
    for item in items:
        book = Book.objects.get(id=item)
        try:
            order = Order(user=request.user, book=book)
            order.clean()
            order.save()
            success_orders.append(order)
        except ValidationError as e:
            error_orders.append({'object': book, 'error': e})

    context = {
                'success_orders': success_orders,
                'error_orders': error_orders
              }
    request.user.clear_cart()
    return render(request, 'Orders/order_report.html', context=context)



