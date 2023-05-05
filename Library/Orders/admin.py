from django.contrib import admin

from .models import Order

# Register your models here.


@admin.register(Order)
class CustomOrderAdmin(admin.ModelAdmin):
    actions = ['make_complete', 'make_cancel']
    search_fields = ['id', 'user__username', 'user__document_seria',
                     'user__first_name', 'user__last_name']
    list_display = ('__str__', 'created_at', 'expires_in', 'status')
    fields = ('user', 'book', 'status')

    def make_complete(self, request, queryset):
        queryset.update(status='complete')

    def make_cancel(self, request, queryset):
        queryset.update(status='canceled')

    make_complete.short_description = "Выполнить выбранные заказы"
    make_cancel.short_description = "Отменить выбранные заказы"


