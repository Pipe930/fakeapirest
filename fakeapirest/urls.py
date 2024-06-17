from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.user.urls import urls_users
from apps.user.views import LoginView, LogoutView, TokenRefreshView

urls_api = [

    path("users/", include(urls_users)),
    path("auth/login", LoginView.as_view(), name="loginuser"),
    path("auth/logout", LogoutView.as_view(), name="logoutuser"),
    path("token-jwt/refresh", TokenRefreshView.as_view(), name="refreshtoken")
]

urlpatterns = [
    #path('admin/', admin.site.urls),
    path("api/v1.0/", include(urls_api))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
