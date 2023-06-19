from django.urls import path
# Импортируем созданные нами представления
from .views import PostList, PostDetail, PostSearch, PostCreate, PostEdit, PostDelete, NewsCreate, NewsEdit, NewsDelete, subscriptions

from django.views.decorators.cache import cache_page

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.

   # path('news/', cache_page(60)(PostList.as_view()), name='post_list'),# Добавим кэширование главной страницы на 1 минуту
   path('news/', PostList.as_view(), name='post_list'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   # path('news/<int:pk>', cache_page(60*5)(PostDetail.as_view()), name='post_detail'), # Добавим кэширование страницы с деталями поста на 5 минуту
   path('news/<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('news/search/', PostSearch.as_view(), name='post_search'),

   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),

   path('articles/create/', PostCreate.as_view(), name='post_create'),
   path('articles/<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
   path('articles/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('subscriptions/', subscriptions, name='subscriptions'),
   # path('categories/<int:pk>', CategoryListView.as_view, name='category_list'),
   # path('hello/', IndexView.as_view(), name='hello'),

]
