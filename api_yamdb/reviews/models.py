from django.db import models

from core.models import PostModel


class Review(PostModel):
    SCORES = [
        ("1", 1),
        ("2", 2),
        ("3", 3),
        ("4", 4),
        ("5", 5),
        ("6", 6),
        ("7", 7),
        ("8", 8),
        ("9", 9),
        ("10", 10)
    ]

    title_id = models.IntegerField()  # Позднее изменится на ForeignKey
    score = models.IntegerField(choices=SCORES)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title_id', 'author'],
                name='unique_title_id_author'
            )
        ]

    def __str__(self):
        return (f'{self.author} отозвался о произведении '
                f'{self.title_id}: "{self.text}".')


class Comment(PostModel):
    review_id = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )

    def __str__(self):
        return (f'{self.author} прокомментиовал отзыв '
                f'{self.review_id}: "{self.text}".')
