from django.db import models


class ClassificationModel(models.Model):
    """Добавляет наименование и слаг."""
    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class PostModel(models.Model):
    """Добавляет текст и дату публикации."""
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        abstract = True
