# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login as django_login, logout as django_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _

from articles.models import Article, Favourite
from users.models import Follower
from users.forms import LoginForm, SignupForm, UserModelForm, UserProfileModelForm, SetPasswordForm
from users.models import UserProfile

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from welldone.settings import DEFAULT_FROM_EMAIL, SITE_DOMAIN
from django.views.generic import *
from users.forms import PasswordResetRequestForm
from django.db.models.query_utils import Q


class LoginView(View):
    def get(self, request):
        """
        Presents user login
        :param request: HttpRequest object with request data
        :return: HttpResponse object with response data
        """
        if request.user.is_authenticated:
            return redirect(request.GET.get("next", "welldone_home"))
        login_form = LoginForm()
        context = {"form": login_form}
        return render(request, "users/login.html", context)

    def post(self, request):
        """
        Manage user access
        :param request: HttpRequest object with request data
        :return: HttpResponse object with response data
        """
        error_message = ""
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get("username")
            password = login_form.cleaned_data.get("pwd")
            user = authenticate(username=username,
                                password=password)  # authenticate just retrieves user from BD
            if user is None:
                error_message = _(u"Usuario o contraseña incorrecta")
            else:
                if user.is_active:
                    django_login(request, user)  # Assign authenticated user to request object
                    return redirect(request.GET.get("next", "welldone_home"))
                else:
                    error_message = _(u"User inactive")

        context = {"error": error_message, "form": login_form}
        return render(request, "users/login.html", context)


class SigninView(View):
    def get(self, request):
        """
        Presents user signup form
        :param request: HttpRequest object with request data
        :return: HttpResponse object with response data
        """
        error_message = ""
        signup_form = SignupForm()
        context = {"error": error_message, "form": signup_form}
        return render(request, "users/signup.html", context)

    def post(self, request):
        """
        Validate register data and create new user
        :param request: HttpRequest object with request data
        :return: HttpResponse object with response data
        """
        signin_form = SignupForm(request.POST)
        if signin_form.is_valid():
            encrypted_pass = make_password(signin_form.cleaned_data["password"])
            signin_form.instance.password = encrypted_pass
            signin_form.save()
            user = authenticate(username=signin_form.cleaned_data["username"],
                                password=signin_form.cleaned_data["password"])  # authenticate just retrieves user from BD
            django_login(request, user)  # Assign authenticated user to request object
            return redirect(request.GET.get("next", "welldone_home"))

        context = {"form": signin_form}
        return render(request, "users/signup.html", context)


class LogoutView(View):
    def get(self, request):
        """
        Performs logout
        :param request: HttpRequest object with request data
        :return: redirects to home
        """
        if request.user.is_authenticated():
            django_logout(request)
        return redirect("welldone_home")


class ProfileView(View):
    def get(self, request, username):
        """
        Presents user profile and list of articles
        :param request: HttpRequest object with request data
        :return: HttpResponse object with response data
        """

        user = User.objects.filter(username=username).select_related("user")
        if len(user) == 0 or (not request.user.is_superuser and user[0].is_staff):
            return render(request, 'users/profile.html', {'error_message': _(u"Usuario no encontrado, lo sentimos mucho 😢")})

        follow = ""
        following_class = ""
        if request.user.is_authenticated:
            follow = Follower.objects.filter(user=request.user, followed=user)
        if len(follow) > 0:
            following_class = "following"
        else:
            following_class = "follow"

        order = request.GET.get('order')
        if order == 'asc':
            orden_list = ''
        else:
            orden_list = '-'

        article = Article.objects.all().select_related("user")
        article = article.filter(user=user)
        if not request.user.is_superuser and user[0] != request.user:
            article = article.filter(publication_date__lt=datetime.now())
        article = article.order_by(orden_list+'create_date')

        if bool(user[0].user.photo):
            photo = user[0].user.photo.url
        else:
            photo = None

        favourites = ""
        if request.user.is_authenticated:
            favourites = Favourite.objects.filter(user=request.user)

        if len(favourites) > 0:
            for post in article:
                if any(favourite.article == post for favourite in favourites):
                    post.favourite_article = 'fa-heart'

        page = request.GET.get('page', 1)
        paginator = Paginator(article, 10)

        try:
            article = paginator.page(page)
        except PageNotAnInteger:
            article = paginator.page(1)
        except EmptyPage:
            article = paginator.page(paginator.num_pages)

        return render(request, 'users/profile.html', {'articles_list': article,
                                                      'bio': user[0].user.bio,
                                                      'photo': photo,
                                                      'username': user[0].username,
                                                      'following_class': following_class,
                                                      'id_user': user[0].id,
                                                      'name': u'{first} {last}'.format(first=user[0].first_name,
                                                                                       last=user[0].last_name)})


class Followers(View):
    @staticmethod
    def getcontext(request, follow_user, followed_user):
        if follow_user:
            following_users = Follower.objects.filter(user__username=follow_user).select_related("user")
            for user in following_users:
                user.following_class = "following"
                user.user = user.followed
            return {"user_list": following_users,
                    "title": _(u"Usuarios a los que sigues")}
        elif followed_user:
            following_users = Follower.objects.filter(user=request.user).select_related("user")
            followed_users = Follower.objects.filter(followed__username=followed_user).select_related("user")
            for user in followed_users:
                if any(user_following.followed == user.user for user_following in following_users):
                    user.following_class = "following"
            return {"user_list": followed_users,
                    "title": _(u"Usuarios que te siguen")}

    @method_decorator(login_required)
    def get(self, request, follow_user=None, followed_user=None):
        return render(request, "users/user_list_simple.html", self.getcontext(request, follow_user, followed_user))


@login_required
def edit_user(request):
    user = request.user
    user_form = UserModelForm(instance=user)
    profile_inline_formset = inlineformset_factory(User,
                                                   UserProfile,
                                                   fields=('bio', 'photo'),
                                                   can_delete=False,
                                                   form=UserProfileModelForm)
    formset = profile_inline_formset(instance=user)

    if request.user.is_authenticated():
        message = ""
        if request.method == "POST":
            user_form = UserModelForm(request.POST, request.FILES, instance=user)
            formset = profile_inline_formset(request.POST, request.FILES, instance=user)
            message = _(u'😭 Ha ocurrido un error al guardar la información. Inténtalo mas tarde. ')
            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = profile_inline_formset(request.POST, request.FILES, instance=created_user)
                if formset.is_valid():
                    if user_form.save():
                        if formset.save():
                            message = _(u'Información actualizada.')
                            return HttpResponseRedirect(
                                reverse('user_profile', args=[user]))

        return render(request, "users/update.html", {
            "form": user_form,
            "formset": formset,
            "message": message,
        })
    else:
        raise PermissionDenied


class ResetPasswordRequestView(View):

    @staticmethod
    def validate_email_address(email):
        '''
        This method here validates the if the input is an email address or not. Its return type is boolean, True if the input is a email address or False if its not.
        '''
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def get(self, request):
        """
        Presents user login
        :param request: HttpRequest object with request data
        :return: HttpResponse object with response data
        """
        messages = None
        reset_pwd_form = PasswordResetRequestForm()
        context = {"messages": messages,
                    "form": reset_pwd_form}
        return render(request, "users/reset_password.html", context)

    def post(self, request):
        '''
            A normal post request which takes input from field "email_or_username" (in ResetPasswordRequestForm).
        '''
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data["email_or_username"]
        if self.validate_email_address(data) is True:  # uses the method written above
            '''
            If the input is an valid email address, then the following code will lookup for users associated with that email address. If found then an email will be sent to the address, else an error message will be printed on the screen.
            '''
            associated_users = User.objects.filter(Q(email=data) | Q(username=data))
            if associated_users.exists():
                for user in associated_users:
                        c = {
                            'email': user.email,
                            'domain': request.META['HTTP_HOST'],
                            'site_name': 'your site',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'user': user,
                            'token': default_token_generator.make_token(user),
                            'protocol': 'http',
                            }
                        email_template_name = 'users/reset_pwd_email.html'
                        subject = _(u"Recuperar contraseña | Welldone")  # loader.render_to_string(subject_template_name, c)
                        # Email subject *must not* contain newlines
                        subject = ''.join(subject.splitlines())
                        email = loader.render_to_string(email_template_name, c)
                        send_mail(subject, email, DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)

                form = PasswordResetRequestForm()
                messages = _(u'Hemos enviado un email a ' + data + u". Por favor, comprueba tu bandeja de entrada para continuar con la recuperación de la contraseña.")
                context = {"messages": messages,
                           "form": form}
                return render(request, "users/reset_password.html", context)

            messages = _(u'Este usuario no tiene ningún email asociado.')
            context = {"messages": messages,
                       "form": form}
            return render(request, "users/reset_password.html", context)

        else:
            '''
            If the input is an username, then the following code will lookup for users associated with that user. If found then an email will be sent to the user's address, else an error message will be printed on the screen.
            '''
            associated_users = User.objects.filter(username=data)
            if associated_users.exists():
                for user in associated_users:
                    c = {
                        'email': user.email,
                        'domain': SITE_DOMAIN,  #or your domain
                        'site_name': 'Welldone',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                        }

                    email_template_name = 'users/reset_pwd_email.html'
                    subject = _(u"Recuperar contraseña | Welldone") #loader.render_to_string(subject_template_name, c)
                    # Email subject *must not* contain newlines
                    subject = ''.join(subject.splitlines())
                    email = loader.render_to_string(email_template_name, c)
                    send_mail(subject, email, DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)

                form = PasswordResetRequestForm()
                messages = _(u"Se ha mandado un correo al usuario ")  + data + _(u". Por favor, revisa tu correo.")
                context = {"messages": messages,
                           "form": form}
                return render(request, "users/reset_password.html", context)


            messages = _(u'Este usuario no existe.')
            context = {"messages": messages,
                       "form": form}
            return render(request, "users/reset_password.html", context)

        messages = _(u'Entrada inválida')
        context = {"messages": messages,
                   "form": form}
        return render(request, "users/reset_password.html", context)


class PasswordResetConfirmView(View):

    def get(self, request, uidb64, token):
        """
        Presents user login
        :param request: HttpRequest object with request data
        :return: HttpResponse object with response data
        """
        confirm_pwd_form = SetPasswordForm()
        context = {"form": confirm_pwd_form}
        return render(request, "users/confirm_password.html", context)

    def post(self, request, uidb64=None, token=None):
        """
        View that checks the hash in a password reset link and presents a
        form for entering a new password.
        """
        UserModel = get_user_model()
        form = SetPasswordForm(request.POST)
        assert uidb64 is not None and token is not None  # checked by URLconf
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password = form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()

                form = SetPasswordForm()
                messages = _(u'La contraseña ha sido actualizada.')
                context = {"messages": messages,
                           "form": form}
                return render(request, "users/reset_password.html", context)
            else:
                messages = _(u'No se ha podido actualizar la contraseña.')
                form = SetPasswordForm(request.POST)
                context = {"messages": messages,
                           "form": form}
                return render(request, "users/reset_password.html", context)
        else:
            messages = _(u'Este link para reiniciar la contraseña ya no es válido.')
            form = SetPasswordForm(request.POST)
            context = {"messages": messages,
                       "form": form}
            return render(request, "users/reset_password.html", context)
