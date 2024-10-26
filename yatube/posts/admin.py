from django.contrib import admin
from .models import Post, Group


admin.site.register(Post)
admin.site.register(Group)


class PostAdmin(admin.ModelAdmin):
    list_display = ('text', 'pub_date', 'author', 'group',)
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
