from django.contrib import admin

from .models import BookType, BookRubric, Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'rubric', 'count', 'is_available')
    fields = ('is_available', 'name', 'rubric', 'type', 'authors',
              'created_year', 'created_place', 'pages_count',
              'price', 'count', 'image')


@admin.register(BookType)
class BookTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'time_limit')
    fields = ('name', 'time_limit', 'forfeit')



@admin.register(BookRubric)
class BookRubricAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name', 'description')