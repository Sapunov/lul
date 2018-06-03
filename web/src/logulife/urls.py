from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from logulife.web.views import index


urlpatterns = [
    path('api/', include('logulife.api.urls')),
    path('<path>', index),
    path('', index)
]

if settings.ADMIN_ENABLED:
    urlpatterns.insert(0, path('admin/', admin.site.urls))
