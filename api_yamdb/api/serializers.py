from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Review, Comment


class ReviewSerializer(serializers.ModelSerializer):
    # title_id = SlugRelatedField(slug_field='name', read_only=True)
    # author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['title_id', 'author'],
                message='Вы уже оставляли отзыв.'
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    # author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
