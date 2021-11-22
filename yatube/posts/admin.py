from django.contrib import admin

from .models import Comment, Post, Group, Follow


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


class CommentAdmin(admin.ModelAdmin):
    '''
    Класс CommentAdmin.
    Настройка отображения комментариев к постам при администрировании.
    '''
    list_display = ('pk', 'post', 'author', 'text', 'created')
    search_fields = ('post', 'author')
    list_filter = ('created', 'author',)
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    '''
    Класс FollowAdmin.
    Настройка отображения подписок при администрировании.
    '''
    list_display = ('pk', 'user', 'author')
    search_fields = ('user', 'author')
    list_filter = ('author', 'user')
    empty_value_display = '-пусто-'


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)
