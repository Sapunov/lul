from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from logulife.web.views import index


urlpatterns = [
    path('api/tokens', obtain_auth_token),
    path('api/records', include('logulife.records.urls')),
    path('api/spender', include('logulife.spender.urls')),
    path('<path>', index),
    path('', index)
]

if settings.ADMIN_ENABLED:
    urlpatterns.insert(0, path('admin/', admin.site.urls))
