from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from articles.api import ArticleViewSet, CommentsViewSet, FavouriteViewSet
from articles.views import FavouriteListView, ArticleEditView, ArticleView, ArticleListView, InstallDb, ArticleCreateView, \
    ArticleDeleteView


router = DefaultRouter()
router.register(r'api/1.0/articles', ArticleViewSet, base_name="api_articles")
router.register(r'api/1.0/articles/(?P<idArticle>[0-9]+)/comments', CommentsViewSet, base_name="api_comments")
router.register(r'api/1.0/favorites', FavouriteViewSet, base_name="api_favorites")

urlpatterns = [
    url(r'^$', ArticleListView.as_view(), name='welldone_home'),
    url(r'^articles/category/(?P<category>[A-Za-z0-9\-]+)$', ArticleListView.as_view(), name='list_articles_category'),
    url(r'^articles/@(?P<username>\w+)/$', ArticleListView.as_view(), name='list_articles_user'),
    url(r'^@(?P<username>\w+)/(?P<pk>[0-9]+)$', ArticleView.as_view(), name='article_details'),
    url(r'^article/create$', ArticleCreateView.as_view(), name='article_create'),
    url(r'^article/(?P<pk>[0-9]+)/edit', ArticleEditView.as_view(), name='article_edit'),
    url(r'^article/(?P<pk>[0-9]+)/delete', ArticleDeleteView.as_view(), name='article_delete'),


    url(r'^@(?P<username>\w+)/favourites/$', FavouriteListView.as_view(), name='list_favourites_user'),
    url(r'^install/$', InstallDb.as_view(), name='install_BD'),

    # API URLS
    url(r'', include(router.urls), name='api_articles'),
    #url(r'^api/1.0/comments/$', CommentsApi.as_view(), name='api_posts_list')
]
