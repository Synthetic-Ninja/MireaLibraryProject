from django.db import models
from datetime import date
import re


class BookType(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=128, unique=True)
    # Ограничение времени владения книгой, выраженное целым числом дней
    time_limit = models.PositiveIntegerField(default=0)
    # Размер штрафа для типа книги
    forfeit = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f'[{self.id}] - {self.name}'


class BookRubric(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField()

    def __str__(self):
        return f'[{self.id}] - {self.name}'


class Book(models.Model):
    id = models.BigAutoField(primary_key=True)
    is_available = models.BooleanField()
    image = models.ImageField(upload_to='books_images')
    name = models.CharField(max_length=256, unique=True)
    rubric = models.ForeignKey(to=BookRubric, on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey(to=BookType, on_delete=models.CASCADE)
    authors = models.TextField()
    created_year = models.PositiveIntegerField()
    created_place = models.CharField(max_length=128)
    pages_count = models.PositiveIntegerField()
    # Цена выражена числом Decimal с 11 цифрами и 2 знаками после запятой
    price = models.DecimalField(max_digits=11, decimal_places=2)
    count = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def increment_count(self) -> None:
        self.count += 1
        super().save()

    def decrement_count(self) -> None:
        self.count -= 1
        super().save()

    def get_created_year(self) -> str:
        return str(self.created_year) \
            if ((date.today().year - int(self.created_year)) <= 20) \
            else f'{self.created_year} (Старое издание)'

    def get_created_place(self) -> str:
        keywords = {
                    'М': 'Москва',
                    'Л': 'Ленинград',
                    'Мн': 'Минск',
                    'К':  'Киев',
                    'СПб': 'Санкт-Петербург'
                    }
        return keywords.get(str(self.created_place), self.created_place)

    def get_author(self) -> str:
        pattern = r'[А-Яа-я]+\s[А-Яа-я]+\s[А-Яа-я]\s*'
        if re.search(pattern, self.authors):
            author = self.authors.split()
            return f'{author[0]} {author[1][:1]}.{author[2][:1]}.'
        return self.authors