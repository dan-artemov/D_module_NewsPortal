from django_filters import FilterSet, ModelMultipleChoiceFilter, CharFilter, DateTimeFilter, ModelChoiceFilter
from django.forms import DateTimeInput
from .models import Post, Category

# Создаем свой набор фильтров для модели Post.

class PostFilter(FilterSet):

    # post_type = ModelChoiceFilter(
    #     field_name='post_type',
    #     queryset=Post.objects.all(),
    #     label='Тип: новость/статья',
    #     # lookup_expr='icontains',
    # )

    # post_type = CharFilter(
    #     field_name='post_type',
    #     label='Тип: новость/статья',
    #     lookup_expr='icontains',
    # )


    header = CharFilter(
        field_name='post_header',
        label='Заголовок',
        lookup_expr='icontains',
    )
    cat = ModelMultipleChoiceFilter(

        field_name='categories',
        queryset=Category.objects.all(),
        label='Категория',
        conjoined=True,
    )

    added_after = DateTimeFilter(
        field_name='data_create',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},

        ),
        label='Дата, после которой опубликована статья',
    )

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            'post_type',
        }

