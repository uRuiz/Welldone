# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.utils.datetime_safe import datetime
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views import View

from articles.forms import ArticleForm
from articles.models import Article, Category, Favourite
from users.models import Follower


class ArticleView(View):

    @staticmethod
    def get_article_by_pk_owner(user, logged_user, pk):
        article = Article.objects.all().select_related("user")
        if logged_user.is_superuser or user[0] == logged_user:
            article = article.filter(user=user, pk=pk)
        else:
            article = article.filter(publication_date__lt=datetime.now(), user=user, pk=pk).order_by('-create_date')
        return article

    def get(self, request, username, pk):
        """
        Pinta la vista detalle de un post
        :param request: objeto HttpRequest con los datos de la petición
        :param username: el nombre del usuari propietario del post
        :param pk: el id del posts a visualizar
        :return: objeto HttpResponse con los datos de la respuesta
        """
        article = self.get_article_by_pk_owner(User.objects.filter(username=username), request.user, pk)

        if len(article) == 0:
            return HttpResponseNotFound(_(u"No hemos encontrado este artículo"))
        elif len(article) > 1:
            return HttpResponseNotFound(_(u"No hemos encontrado este artículo"))
        else:
            article[0].responses_count = len(Article.objects.filter(article_answered=article[0].pk))
            list_respuestas = Article.objects.filter(article_answered=article[0].pk)

            follow = ""
            favourite = ""
            if request.user.is_authenticated:
                follow = Follower.objects.filter(user=request.user, followed=article[0].user)
                favourite = Favourite.objects.filter(user=request.user, article=article)
            if len(follow) > 0:
                following_class = "following"
            else:
                following_class = "follow"
            if len(favourite) > 0:
                favourite_class = 'fa-heart'
            else:
                favourite_class = 'fa-heart-o'
            return render(request, 'articles/detail.html', {'article': article[0],
                                                            'following_class': following_class,
                                                            'favourite_class': favourite_class,
                                                            'articles_list_resp': list_respuestas})


class ArticleCreateView(View):
    @method_decorator(login_required)
    def get(self, request):
        """
        :param request:
        :return:
        """
        response_title = None
        article_form = ArticleForm()
        id_response_article = request.GET.get('responseFrom')

        if id_response_article is not None:
            response_article = Article.objects.filter(pk=id_response_article).select_related("user")
            response_title = '@' + response_article[0].user.username + ' / ' + response_article[0].title

        context = {'form': article_form,
                   'response_id': id_response_article,
                   'response_title': response_title,
                   'message': ""}

        return render(request, 'articles/create.html', context)

    @method_decorator(login_required)
    def post(self, request):
        """

        :param request:
        :return:
        """
        error_message = None
        response_article = Article.objects.filter(pk=request.POST.get("id_article_answered"))
        if len(response_article) > 0:
            article_with_data = Article(user=request.user, article_answered=response_article[0])
        else:
            article_with_data = Article(user=request.user)
        article_form = ArticleForm(request.POST, request.FILES, instance=article_with_data)

        if article_form.is_valid():
            new_article = article_form.save()
            return HttpResponseRedirect(reverse('article_details', args=[new_article.user.username, new_article.pk]))

        context = {'form': article_form,
                   'message': error_message}

        return render(request, 'articles/create.html', context)


class ArticleEditView(View):
    @method_decorator(login_required)
    def get(self, request, pk):
        """

        :param request:
        :return:
        """
        post = Article.objects.all().filter(pk=pk)
        article_form = ArticleForm(instance=post[0])

        context = {'form': article_form,
                   'message': ""}

        return render(request, 'articles/create.html', context)

    @method_decorator(login_required)
    def post(self, request, pk):
        """

        :param request:
        :return:
        """
        error_message = None

        post = Article.objects.all().filter(pk=pk)
        article_form = ArticleForm(request.POST, request.FILES, instance=post[0])

        if article_form.is_valid():
            update_article = article_form.save()
            return HttpResponseRedirect(reverse('article_details', args=[update_article.user.username, update_article.pk]))

        context = {'form': article_form,
                   'message': error_message}

        return render(request, 'articles/create.html', context)


class ArticleDeleteView(View):
    @method_decorator(login_required)
    def get(self, request, pk):
        """

        :param request:
        :return:
        """

        post = Article.objects.all().filter(pk=pk)
        if request.user == post[0].user:
            post.delete()
            return HttpResponseRedirect(reverse('list_articles_user', args=[request.user]))


class ArticleListView(View):

    def get(self, request, category=None, username=None):
        posts = Article.objects.all().select_related("user").prefetch_related("categories")

        page = request.GET.get('page', 1)

        order = request.GET.get('order')
        if order == 'asc':
            orden_list = ''
        else:
            orden_list = '-'

        favourites = ""
        if request.user.is_authenticated:
            favourites = Favourite.objects.filter(user=request.user)

        if category is not None:
            posts = posts.filter(categories__name=category, publication_date__lt=datetime.now()).order_by(orden_list+'publication_date')

        elif username is not None:
            posts = posts.filter(user__username=username, publication_date__lt=datetime.now()).order_by(orden_list+'publication_date')

        else:
            posts = posts.filter(publication_date__lt=datetime.now()).order_by(orden_list+'publication_date')

        paginator = Paginator(posts, 10)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        if len(favourites) > 0:
            for post in posts:
                if any(favourite.article == post for favourite in favourites):
                    post.favourite_article = 'fa-heart'

        return render(request, 'articles/list.html', {'articles_list': posts})


class InstallDb(View):
    def get(self, request):
        categories = ['startup', 'marketing',
                      'productivity', 'design', 'copywriting']

        for element in categories:
            categories = Category.objects.all().filter(name=element)
            if len(categories) == 0:
                category = Category(name=element)
                category.save()

        return HttpResponse('BDD actualizada')


class FavouriteListView(View):

    @staticmethod
    def get_favourites_by_user(user, username, orden_list):
        favourites = Favourite.objects.all().filter(user__username=username).select_related("article").select_related("user")\
            .order_by(orden_list+'article__article__publication_date')

        return favourites

    @method_decorator(login_required)
    def get(self, request, username):
        page = request.GET.get('page', 1)
        order = request.GET.get('order')
        if order == 'asc':
            orden_list = ''
        else:
            orden_list = '-'

        my_favourites_list = self.get_favourites_by_user(request.user, username, orden_list)

        paginator = Paginator(my_favourites_list, 10)
        try:
            my_favourites_list = paginator.page(page)
        except PageNotAnInteger:
            my_favourites_list = paginator.page(1)
        except EmptyPage:
            my_favourites_list = paginator.page(paginator.num_pages)

        post_favourites = []
        for post in my_favourites_list:
            post.article.favourite_article = 'fa-heart'
            post_favourites.append(post.article)

        context = {
            'favourites_list': post_favourites,
        }
        return render(request, 'articles/favourites.html', context)
