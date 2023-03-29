from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import ReviewViewSet, CommentViewSet


router = DefaultRouter()
router.register(r'reviews', ReviewViewSet)
# router.register(r'titles/(?P<title_id>\d+)/reviews',
#                 ReviewViewSet,
#                 basename='rewiews')
# router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
#                 CommentViewSet,
#                 basename='comments')
router.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
]
