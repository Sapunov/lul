from django.urls import path

from app.records.views import (
    RecordsView, SingleRecordView, RecordsLabelsListView,
    LableSetView, LabelConfirmView)


urlpatterns = [
    path('', RecordsView.as_view()),
    path('/labels', RecordsLabelsListView.as_view()),
    path('/<record_id>', SingleRecordView.as_view()),
    path('/<record_id>/label', LableSetView.as_view()),
    path('/<record_id>/label/confirm', LabelConfirmView.as_view()),
]
