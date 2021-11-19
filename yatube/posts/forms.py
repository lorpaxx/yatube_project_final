from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    '''
    Класс для формы нового поста.
    '''
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')

    def clean_text(self):
        '''
        Функция валидации поля text.
        '''
        data = self.cleaned_data['text']
        if not data:
            raise forms.ValidationError('Это поле не заполнено!')
        return data


class CommentForm(forms.ModelForm):
    '''
    Класс для формы нового комментария.
    '''
    class Meta:
        model = Comment
        fields = ('text',)

    def clean_text(self):
        '''
        Функция валидации поля text.
        '''
        data = self.cleaned_data['text']
        if not data:
            raise forms.ValidationError('Это поле не заполнено!')
        return data
