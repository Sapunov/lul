from rest_framework.response import Response
from rest_framework.views import APIView

from logulife.api import serializers
from logulife.api.common import serialize, deserialize
from logulife.api import models


class Records(APIView):

    serializer_class = serializers.Record

    def post(self, request):

        serializer = deserialize(
            self.serializer_class,
            request.data,
            context={'request': request})
        serializer.save()

        return Response(serializer.data)

    def put(self, request):

        # Для проверки всех обязательных полей
        deserialize(serializers.Record, request.data)

        record = models.Record.get_record(
            request.user,
            request.data['source_name'],
            request.data['source_record_id'])

        serializer = serialize(serializers.Record, record, data=request.data)
        serializer.save()

        return Response(serializer.data)
