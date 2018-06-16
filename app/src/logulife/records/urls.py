from django.urls import path

from logulife.records.views import (
    RecordsView, SingleRecordView, RecordsLabelsListView)


urlpatterns = [
    path('', RecordsView.as_view()),
    path('/labels', RecordsLabelsListView.as_view()),
    path('/<record_id>', SingleRecordView.as_view()),
]
