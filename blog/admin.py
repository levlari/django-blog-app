from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    exclude = ('word_count', 'read_time_in_mins')
    prepopulated_fields = {'slug': ('title',)}
