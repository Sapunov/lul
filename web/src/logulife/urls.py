from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from logulife.web import views as web_views


urlpatterns = [
    path('api/', include('logulife.api.urls')),
    path('<path>', web_views.index)
]

if settings.ADMIN_ENABLED:
    urlpatterns.insert(0, path('admin/', admin.site.urls))
