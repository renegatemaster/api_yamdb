from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from core.models import ClassificationModel, PostModel
from users.models import User
from .validators import validate_year


class Category(ClassificationModel):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']


class Genre(ClassificationModel):

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200
    )
    year = models.IntegerField(
        verbose_name='Дата выхода',
        validators=[validate_year]
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        through='GenreTitle'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
    )
    rating = models.IntegerField(
        verbose_name='Рейтинг',
        null=True,
        default=None
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр',
        on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}, жанр - {self.genre}'

    class Meta:
        verbose_name = 'Произведение и жанр'
        verbose_name_plural = 'Произведения и жанры'


class Review(PostModel):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.IntegerField(
        validators=[
            MaxValueValidator(10, 'Значение не должно быть больше 10.'),
            MinValueValidator(1, 'Значение не должно быть меньше 1.')
        ]
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]

    def __str__(self):
        return (f'{self.author} отозвался о произведении '
                f'{self.title}: "{self.text}".')


class Comment(PostModel):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-id']

    def __str__(self):
        return (f'{self.author} прокомментиовал отзыв '
                f'{self.review}: "{self.text}".')
