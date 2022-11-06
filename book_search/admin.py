from django.contrib import admin

# Register your models here.

from .models import Books

class BooksAdmin(admin.ModelAdmin):
    list_display = ("name", "author",)

admin.site.register(Books, BooksAdmin)