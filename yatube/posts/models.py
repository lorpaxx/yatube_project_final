from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Group(models.Model):
    '''
    Класс Group.
    '''
    title = models.CharField(
        max_length=200,
        verbose_name='Группа',
        help_text='Группа, к которой будет относиться пост'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Tag группы',
        help_text='Tag группы'
    )
    description = models.TextField(
        verbose_name='Описание группы',
        help_text='Краткое описание группы'
    )

    def __str__(self):
        '''
        При обращении к экземпляру возвращаем slug для ссылки на группу.
        '''
        return self.title


class Post(models.Model):
    '''
    Класс Post.
    '''
    text = models.TextField(
        verbose_name='Текст поста',
        help_text='Текст нового поста'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время публикации поста',
        help_text='Дата и время публикации поста',
        db_index=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор поста',
        help_text='Автор поста'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts',
        verbose_name='Группа',
        help_text='Группа, к которой будет относиться пост'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        '''
        При обращении к экземпляру возвращаем
        сокращённый text выбранного поста.
        '''
        return self.text[:15]


class Comment(models.Model):
    '''
    Класс Comment.
    '''
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='comments',
        verbose_name='Комментарий',
        help_text='Комментарий к посту'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='comments',
        verbose_name='Автор комментария',
        help_text='Автор комментария'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Текст комментария'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время публикации комментария',
        help_text='Дата и время публикации комментария'
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        '''
        При обращении к экземпляру возвращаем
        сокращённый text выбранного комментария.
        '''
        return self.text[:15]
