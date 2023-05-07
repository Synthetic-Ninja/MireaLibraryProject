from dataclasses import dataclass

from django.shortcuts import render

from .models import BookType, BookRubric, Book
from Orders.models import Order

from django.contrib import admin
from django.conf.urls import url

from django.http import Http404


@dataclass
class PublishingHouse:
    name: str
    books: str


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    change_list_template = 'admin/model_change_list.html'
    list_display = ('name', 'type', 'rubric', 'count', 'is_available', 'is_empty')
    fields = ('is_available', 'is_empty', 'name', 'rubric', 'type', 'authors',
              'created_year', 'created_place', 'pages_count',
              'price', 'count', 'image')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [url('^export/$', self.process_export, name='process_import'), ]
        return custom_urls + urls

    def process_export(self, request):
        if not request.user.is_authenticated:
            raise Http404
        books_group_by_created_place = {}
        data = Book.objects.all()
        for item in data:
            keyword = item.get_created_place()
            book_list = books_group_by_created_place.get(keyword, [])
            item.count_of_demands = Order.objects.filter(book=item).count()
            book_list.append(item)
            books_group_by_created_place[keyword] = book_list

        publishing_house = [PublishingHouse(item, books_group_by_created_place[item])
                            for item in books_group_by_created_place.keys()]

        context = {'publishing_house': publishing_house}

        return render(request, 'admin/report.html', context=context)


@admin.register(BookType)
class BookTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'time_limit')
    fields = ('name', 'time_limit', 'forfeit')


@admin.register(BookRubric)
class BookRubricAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name', 'description')
