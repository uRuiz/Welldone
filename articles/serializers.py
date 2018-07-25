from rest_framework import serializers

from articles.models import Article, Category, Comment, Favourite
from users.serializers import UserCommentSerializer


class ArticleSerializer(serializers.ModelSerializer):
    categories = serializers.StringRelatedField(many=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'media', 'introduction', 'text', 'user',
                  'article_answered', 'publication_date', 'categories')


class ArticlePostSerializer(ArticleSerializer):
    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())

    class Meta(ArticleSerializer.Meta):
        fields = ('id', 'title', 'media', 'introduction', 'text',
                  'article_answered', 'publication_date', 'categories')


class CommentsSerializer(serializers.ModelSerializer):
    user = UserCommentSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('user', 'article', 'text', 'create_date')


class FavouriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favourite
        fields = ('article',)

