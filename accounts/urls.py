from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('team', TeamMemberViewSet)

urlpatterns = [
   
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('', include(router.urls)),
    path("register/", UserRegisterationAPIView.as_view(), name="create-user"),
    path("login/", UserLoginAPIView.as_view(), name="login-user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path("logout/", UserLogoutAPIView.as_view(), name="logout-user"),
    path("user-info", UserAPIView.as_view(), name="user-info"),
    

]

