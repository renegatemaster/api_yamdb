from django.db import models


class PostModel(models.Model):
    """Добавляет текст, автора и дату публикации."""
    text = models.TextField()
    author = models.IntegerField()  # Позднее изменится на ForeignKey
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        abstract = True
