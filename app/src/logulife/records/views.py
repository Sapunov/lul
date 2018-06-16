from django.conf import settings
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from logulife.common import get_logger
from logulife.records.models import Record
from logulife.records.serializers import (
    RecordSerializer, RecordCreateSerializer, RecordIdSerializer,
    RecordUpdateDeleteSerializer, LabelSetSerializer, LabelConfirmSerializer)
from logulife.records.misc import is_true


log = get_logger(__name__)


class RecordsView(GenericAPIView):

    serializer_class = RecordSerializer

    def get(self, request):

        filters = {
            'owner': request.user,
            'deleted': False
        }

        if 'source' in request.query_params:
            filters.update({'source__name': request.query_params['source']})

        if 'labels' in request.query_params:
            labels = [l for l in request.query_params['labels'].split(',') if l]
            if labels:
                if '_any' in labels:
                    filters.update({'label__isnull': False})
                elif '_none' in labels:
                    filters.update({'label__isnull': True})
                else:
                    filters.update({'label__in': labels})

        if 'label_confirmed' in request.query_params:
            label_confirmed = is_true(request.query_params['label_confirmed'])
            filters.update({'label_confirmed': label_confirmed})

        if 'q' in request.query_params:
            filters.update({'text__icontains': request.query_params['q']})

        records = Record.objects.filter(**filters).order_by('-timestamp')

        queryset = self.paginate_queryset(records)
        serializer = self.get_serializer(queryset, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request):

        self.serializer_class = RecordCreateSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_serializer = RecordSerializer(serializer.instance)

        return Response(response_serializer.data)


class SingleRecordView(GenericAPIView):

    def get(self, request, record_id):

        record_id_serializer = RecordIdSerializer(
            data={'record_id': record_id},
            context={'request': request})
        record_id_serializer.is_valid(raise_exception=True)

        record = record_id_serializer.validated_data['record']

        serializer = RecordSerializer(record)

        return Response(serializer.data)

    def put(self, request, record_id):

        data = request.data
        data.update({'record_id': record_id})

        update_serializer = RecordUpdateDeleteSerializer(
            data=data, context={'request': request})
        update_serializer.is_valid(raise_exception=True)
        update_serializer.save()

        record = update_serializer.validated_data['record']
        serializer = RecordSerializer(record)

        return Response(serializer.data)


    def delete(self, request, record_id):

        delete_serializer = RecordIdSerializer(
            data={'record_id': record_id}, context={'request': request})
        delete_serializer.is_valid(raise_exception=True)

        record = delete_serializer.validated_data['record']

        record.archive_record()
        record.notify_delete()

        return Response({'deleted': True})


class RecordsLabelsListView(GenericAPIView):

    def get(self, request):

        return Response({'labels': settings.ALLOWED_LABELS})


class LableSetView(GenericAPIView):

    serializer_class = LabelSetSerializer

    def post(self, request, record_id):

        data = request.data
        data.update({'record_id': record_id})

        if 'force' in request.query_params:
            data.update({'force': True})

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        label = serializer.validated_data['label']
        record = serializer.validated_data['record']

        record.set_label(label, confirm=True)

        return Response({'label': label, 'label_confirmed': True})


class LabelConfirmView(GenericAPIView):

    serializer_class = LabelConfirmSerializer

    def post(self, request, record_id):

        serializer = self.get_serializer(data={'record_id': record_id})
        serializer.is_valid(raise_exception=True)

        label = serializer.validated_data['label']
        record = serializer.validated_data['record']

        record.set_label(label, confirm=True)

        return Response({'label': label, 'label_confirmed': True})
