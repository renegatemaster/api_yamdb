import uuid

from api.filters import TitleFilter
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin,
    ListModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title
from users.models import User

from .paginator import CommentPagination
from .permissions import (
    AuthorAndStaffOrReadOnly,
    IsAdminOrReadOnly,
    OwnerOrAdmins)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    MeSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleGetSerializer,
    TitleSerializer,
    TokenSerializer,
    UserSerializer,
)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg("reviews__score")).all()
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_class = TitleFilter
    ordering_fields = ["id", "name"]
    ordering = ["id"]

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleSerializer
        return TitleGetSerializer

    def get_serializer_class(self):
        if self.request.method in ("POST", "PATCH"):
            return TitleSerializer
        return TitleGetSerializer


class ModelMixinSet(
    CreateModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet
):
    pass


class CategoryViewSet(ModelMixinSet):
    http_method_names = ['get', 'post', 'delete']
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [
        IsAdminOrReadOnly,
    ]
    filter_backends = (
        SearchFilter,
    )
    search_fields = ('name',)


class GenreViewSet(ModelMixinSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [
        IsAdminOrReadOnly,
    ]
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filterset_fields = ("name", "slug")
    ordering_fields = ["id", "name"]
    ordering = ["id"]
    search_fields = ("name", "slug")
    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):
        """Проверка на получение данных"""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        """Проверка на изменение данных"""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorAndStaffOrReadOnly,)
    pagination_class = CommentPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorAndStaffOrReadOnly,)
    pagination_class = CommentPagination

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        return review.comments.all().order_by("id")

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)


@api_view(["POST"])
def signup_post(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data["email"]
    username = serializer.validated_data["username"]
    try:
        user, create = User.objects.get_or_create(
            username=username, email=email)
    except IntegrityError:
        return Response(
            "Такой логин или email уже существуют",
            status=status.HTTP_400_BAD_REQUEST
        )
    confirmation_code = str(uuid.uuid4())
    user.confirmation_code = confirmation_code
    user.save()
    send_mail(
        "Код подверждения",
        confirmation_code,
        ["admin@email.com"],
        (email,),
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def token_post(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data["username"]
    confirmation_code = serializer.validated_data["confirmation_code"]
    user_base = get_object_or_404(User, username=username)
    if confirmation_code == user_base.confirmation_code:
        token = str(AccessToken.for_user(user_base))
        return Response({"token": token}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (OwnerOrAdmins,)
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    search_fields = ("username",)
    ordering_fields = ["id", "username"]
    ordering = ["id"]
    lookup_field = "username"

    @action(
        methods=["get", "patch", "put"],
        detail=False,
        url_path="me",
        permission_classes=(IsAuthenticated,),
    )
    def get_patch_me(self, request):
        user = get_object_or_404(User,
                                 username=self.request.user
                                 )
        serializer_data = {"instance": user,
                           "data": request.data,
                           "partial": False}

        if request.method == "GET":
            serializer = MeSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == "PATCH":
            serializer_data["partial"] = True

        serializer = MeSerializer(**serializer_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserSerializer(instance,
                                    data=request.data,
                                    partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if request.method == "PUT":
            return Response(serializer.data,
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return Response(serializer.data, status=status.HTTP_200_OK)