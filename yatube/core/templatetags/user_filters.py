from django import template


register = template.Library()


@register.filter
def addclass(field, css):
    '''
    Добавляет фильтр addclass.
    '''
    return field.as_widget(attrs={'class': css})
