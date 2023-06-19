from django.db import models
# Импортируем встроенную модель User для создания пользователей и связи с ними
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse

from django.core.cache import cache # Импортируем кэш

class Author(models.Model):
    """Модель Author
        Модель, содержащая объекты всех авторов.
        Имеет следующие поля:
        связь «один к одному» со встроенной моделью пользователей User;
        рейтинг пользователя. Ниже будет дано описание того, как этот рейтинг можно посчитать."""
    user_rating = models.IntegerField(default=0)  # рейтинг пользователя.
    # связь «один к одному» со встроенной моделью пользователей User;
    users = models.OneToOneField(User, related_name='users_id', on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.users}'
    def update_rating(self):
        """Метод update_rating() модели Author, который обновляет рейтинг текущего автора
        (метод принимает в качестве аргумента только self).
        Он состоит из следующего:
            суммарный рейтинг каждой статьи автора умножается на 3;
            суммарный рейтинг всех комментариев автора;
            суммарный рейтинг всех комментариев к статьям автора."""
        au_post_r = self.post_set.aggregate(Sum('post_rating')).get('post_rating__sum')
        au_com_r = self.users.comment_user.aggregate(Sum('comment_rating')).get('comment_rating__sum')
        au_post_com_r = 0

        for i in self.post_set.all():
            au_post_com_r += i.comment_set.aggregate(Sum('comment_rating')).get('comment_rating__sum')

        self.user_rating = au_post_r * 3 + au_com_r + au_post_com_r
        self.save()


class Category(models.Model):
    """Модель Category:
    Категории новостей/статей — темы, которые они отражают (спорт, политика, образование и т. д.).
    Поле должно быть уникальным (в определении поля необходимо написать параметр unique = True)."""
    category = models.CharField(max_length=50, unique=True)  # Имеет единственное поле: название категории
    # Создадим в данной модели поле subscribers - подписчики на категории (возможно ошибка в работе)
    # subscribers = models.ManyToManyField(User, blank=True, related_name='categories')
    def __str__(self):
        return f'{self.category}'

#   В рамках исполнения задания по модулю D6 создадим модель Subscriber для хранения подписок пользователей
class Subscriber(models.Model):
    """Модель Subscriber служит для хранения подписок пользователей
        на выбранные категории статей и содержит два поля:
            user - связь o2m со встроенной моделью User,
            category - связь o2m с моделью Category."""
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )


class Post(models.Model):
    """Модель Post
        Эта модель должна содержать в себе статьи и новости, которые создают пользователи.
        Каждый объект может иметь одну или несколько категорий.
        Соответственно, модель должна включать следующие поля:
        связь «один ко многим» с моделью Author;
        поле с выбором — «статья» или «новость»;
        автоматически добавляемая дата и время создания;
        связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
        заголовок статьи/новости;
        текст статьи/новости;
        рейтинг статьи/новости."""
    article = 'at'
    news = 'nw'
    POST = [
        (article, 'Статья'),
        (news, 'Новости')
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # связь «один ко многим» с моделью Author;
    post_type = models.CharField(max_length=2, choices=POST, default='article')  # поле с выбором — статья или новость
    data_create = models.DateTimeField(auto_now_add=True)  # автоматически добавляемая дата и время создания;
    post_rating = models.IntegerField(default=0)  # рейтинг статьи/новости.
    post_header = models.CharField(max_length=255, default='')  # !!!!!!!!Изменить атрибуты  заголовок статьи/новости;
    post_text = models.TextField(default="")  # текст статьи/новости;
    # связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
    categories = models.ManyToManyField(Category, through='PostCategory')

    def preview(self):
        """Метод preview() возвращает начало статьи (предварительный просмотр) длиной 124 символа
        и добавляет многоточие в конце"""

        return self.post_text[:124] + "..."

    # Методы like() и dislike() увеличивают/уменьшают рейтинг на единицу.
    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()
    def __str__(self):
        return f'{self.post_header}: {self.preview()}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его

class PostCategory(models.Model):
    """Модель PostCategory
        Промежуточная модель для связи «многие ко многим»:
        связь «один ко многим» с моделью Post;
        связь «один ко многим» с моделью Category."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # связь «один ко многим» с моделью Post;
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # связь «один ко многим» с моделью Category.


class Comment(models.Model):
    """Модель Comment.
        Позволяет оставлять комментарии под каждой новостью/статьёй.
        Модель будет иметь следующие поля:
            связь «один ко многим» с моделью Post;
            связь «один ко многим» со встроенной моделью User
            (комментарии может оставить любой пользователь, необязательно автор);
            текст комментария;
            дата и время создания комментария;
            рейтинг комментария."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # связь «один ко многим» с моделью Post;
    # связь «один ко многим» со встроенной моделью User
    user = models.ForeignKey(User, related_name='comment_user', on_delete=models.CASCADE)
    comment = models.TextField(default='')  # !!!!!текст комментария возможно ли пустое поле?;
    data_create = models.DateTimeField(auto_now_add=True)  # !!!!!!!дата и время создания комментария;
    comment_rating = models.IntegerField(default=0)  # рейтинг комментария

    # Методы like() и dislike() увеличивают/уменьшают рейтинг на единицу.
    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()
