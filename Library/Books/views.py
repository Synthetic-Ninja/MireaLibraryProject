from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from .models import Book, BookType, BookRubric


class IndexView(TitleMixin, TemplateView):
    template_name = 'Books/index.html'
    title = 'Book Heaven'


class BookListView(TitleMixin, ListView):
    model = Book
    template_name = 'Books/booklist.html'
    title = 'Book Heaven - Каталог'
    #paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_available=True)
        if book_type := self.request.GET.get('type'):
            queryset = queryset.filter(type=book_type)
        if book_rubric := self.request.GET.get('rubric'):
            queryset = queryset.filter(rubric=book_rubric)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context.update({
            'BookType': BookType.objects.all(),
            'BookRubric': BookRubric.objects.all()
        })
        return context



