from django_filters import FilterSet, DateTimeFilter, CharFilter, ModelChoiceFilter
from django import forms
from django.forms import DateTimeInput
from .models import Post, Author, Category

class PostFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Заголовок содержит'
    )

    author = ModelChoiceFilter(
        field_name='author',
        queryset=Author.objects.all(),
        label='Автор',
        empty_label='Все авторы'
    )


    added_after = DateTimeFilter(
        field_name='time_in',
        lookup_expr='gt',
        label='Опубликовано после',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

class PostForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = [
            'author',
            'categories',
            'title',
            'text',
        ]
        labels = {
            'author': 'Автор',
            'categories': 'Категории',
            'title': 'Заголовок',
            'text': 'Текст статьи/новости',
        }