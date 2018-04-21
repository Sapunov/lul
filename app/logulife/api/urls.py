from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from logulife.api import views


urlpatterns = [
    path('tokens', obtain_auth_token),
    path('records', views.Records.as_view()),
]
