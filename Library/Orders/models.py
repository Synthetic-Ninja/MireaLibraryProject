from django.db import models
from datetime import timedelta, datetime
from decimal import Decimal



from django.core.exceptions import ValidationError


from Users.models import User
from Books.models import Book


def get_expires_data(start_date: datetime.date, days_count: int) -> datetime.date:
    # datetime.date неизменяемый тип данных
    return start_date + timedelta(days_count)


class Order(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создан'),
        ('processing', 'Обработка'),
        ('issued', 'Выдан'),
        ('canceled', 'Отменен'),
        ('overdue', 'Просрочен'),
        ('complete', 'Выполнен')
    ]

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField()
    expires_in = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='created')
    book_is_taken = models.BooleanField(default=False)
    forfeit = models.DecimalField(max_digits=11, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.status == 'issued' and datetime.date(datetime.now()) > self.expires_in:
            self.status = 'overdue'
            self.save()

    def __str__(self):
        return f'Заказ #{self.id} | Пользователь: {self.user.first_name} {self.user.last_name} - \
        [ {self.user.document_seria} {self.user.document_number} ] | Книга [{self.book.name}]'

    def clean(self):
        if not self.book.is_available:
            raise ValidationError('Книгу невозможно добавить в заказ')

        if Order.objects.filter(user=self.user, book_id=self.book, book_is_taken=True) and self.status in ['issued',
                                                                                                           'created',
                                                                                                           'processing']:
            raise ValidationError('Такая книга уже выдана')

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        match self.status:
            case 'created' | 'processing':
                self.expires_in = get_expires_data(self.updated_at, 10)

            case 'issued':
                if not self.book_is_taken:
                    self.book_is_taken = True
                    self.book.decrement_count()
                self.expires_in = get_expires_data(self.updated_at, -1)

            case 'complete' | 'canceled':
                if self.book_is_taken:
                    self.book_is_taken = False
                    self.book.increment_count()
                self.expires_in = self.updated_at

            case 'overdue':
                self.forfeit = self.book.price * self.book.type.forfeit

        super().save(*args, **kwargs)

