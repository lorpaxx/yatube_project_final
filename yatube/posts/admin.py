from django.contrib import admin

from .models import Post, Group


class PostAdmin(admin.ModelAdmin):
    '''
    Класс PostAdmin.
    Настройка отображения постов при администрировании.
    '''
    list_display = ('pk', 'text', 'pub_date', 'author', 'group')
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class GroupAdmin(admin.ModelAdmin):
    '''
    Класс GroupAdmin.
    Настройка отображения групп постовв при администрировании.
    '''
    list_display = ('pk', 'title', 'slug', 'description')
    search_fields = ('title', 'description')
    list_filter = ('slug',)
    empty_value_display = '-пусто-'


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
