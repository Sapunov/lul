from django.urls import path

from logulife.api import views


urlpatterns = [
    path('records', views.Records.as_view()),
]
