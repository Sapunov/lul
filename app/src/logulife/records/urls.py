from django.urls import path

from logulife.records.views import RecordsView, SingleRecordView


urlpatterns = [
    path('', RecordsView.as_view()),
    path('/<record_id>', SingleRecordView.as_view())
]
