from rest_framework import viewsets

from reviews.models import Review, Comment
from api.serializers import ReviewSerializer, CommentSerializer
from api.permissions import IsAuthorOrStaffOrReadOnly


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrStaffOrReadOnly, )

    # def get_queryset(self):
    #     title_id = self.kwargs.get('title_id')
    #     queryset = Review.objects.filter(title_id=title_id)
    #     return queryset

    # def perform_create(self, serializer):
    #     title_id = get_object_or_404(Title, id=self.kwargs.get('title_id'))
    #     serializer.save(author=self.request.user, title_id=title_id)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrStaffOrReadOnly, )

    # def get_queryset(self):
    #     review_id = self.kwargs.get('review_id')
    #     queryset = Comment.objects.filter(review_id=review_id)
    #     return queryset

    # def perform_create(self, serializer):
    #     review_id = get_object_or_404(Review, id=self.kwargs.get('review_id'))
    #     serializer.save(author=self.request.user, review_id=review_id)
