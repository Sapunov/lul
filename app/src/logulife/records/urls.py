from django.urls import path

from .views import Records


urlpatterns = [
    path('', Records.as_view()),
]
