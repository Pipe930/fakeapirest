from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.user.urls import urls_users

urls_api = [

    path("users/", include(urls_users))
]

urlpatterns = [
    #path('admin/', admin.site.urls),
    path("api/v1.0/", include(urls_api))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
