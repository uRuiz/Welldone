from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from users import views
from users.api import UserViewSet, FollowUserViewSet
from users.views import LoginView, SigninView, LogoutView, ProfileView, Followers, ResetPasswordRequestView, \
    PasswordResetConfirmView
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('follow', FollowUserViewSet)

urlpatterns = [
    # API URLS
    url(r'^api/1.0/', include(router.urls)),
    #Web urls
    url(r'^login$', LoginView.as_view(), name='users_login'),
    url(r'^signin$', SigninView.as_view(), name='users_signin'),
    url(r'^logout$', LogoutView.as_view(), name='users_logout'),
    url(r'^profile/@(?P<follow_user>\w+)/following', Followers.as_view(), name='list_user_following'),
    url(r'^profile/@(?P<followed_user>\w+)/followed', Followers.as_view(), name='list_user_followed'),
    url(r'^profile$', views.edit_user, name='users_update'),
    url(r'^@(?P<username>\w+)$', ProfileView.as_view(), name='user_profile'),

    url(r'^reset_password$', ResetPasswordRequestView.as_view(), name="reset_password"),
    url(r'^account/reset_password_confirm/(?P<uidb64>.+)/(?P<token>.+)$', PasswordResetConfirmView.as_view(),
        name='reset_password_confirm'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
