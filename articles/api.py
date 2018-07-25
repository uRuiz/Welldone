from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets, mixins
from articles.models import Article, Comment, Favourite

from articles.permissions import UserPermissionOnArticles
from articles.serializers import ArticleSerializer, ArticlePostSerializer, CommentsSerializer, FavouriteSerializer


class ArticleViewSet(ModelViewSet):

    serializer_class = Article
    permission_classes = (UserPermissionOnArticles,)
    queryset = Article.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ArticlePostSerializer
        else:
            return ArticleSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class CommentsViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Comment.objects.all().select_related("user")
    serializer_class = CommentsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_url_kwarg = "idArticle"

    def paginate_queryset(self, queryset, view=None):
        #disable pagination
        return None

    def get_queryset(self):
        idArticle = self.kwargs.get(self.lookup_url_kwarg)
        if self.action in ['list']:
            return self.queryset.filter(article__id=idArticle).order_by('-create_date')

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class FavouriteViewSet(ModelViewSet):

    queryset = Favourite.objects.all()
    serializer_class = Favourite
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ['create', 'destroy']:
            return FavouriteSerializer

    def perform_create(self, serializer):
        follows = Favourite.objects.filter(article=serializer.validated_data.get("article"), user=self.request.user.id)
        if follows.count() > 0:
            return follows.delete()
        else:
            return serializer.save(user=self.request.user)
