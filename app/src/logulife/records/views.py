from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RecordSerializer
from logulife.common import serialize, deserialize
from .models import Record


class Records(APIView):

    serializer_class = RecordSerializer

    def get(self, request):

        records = Record.objects.filter(owner=request.user)
        serializer = serialize(self.serializer_class, records, many=True)

        return Response(serializer.data)

    def post(self, request):

        serializer = deserialize(
            self.serializer_class,
            request.data,
            context={'request': request})
        serializer.save()

        return Response(serializer.data)

    def put(self, request):

        # Для проверки всех обязательных полей
        deserialize(self.serializer_class, request.data)

        record = Record.get_record(
            request.user,
            request.data['source_name'],
            request.data['source_record_id'])

        # call update
        serializer = serialize(self.serializer_class, record, data=request.data)
        serializer.save()

        return Response(serializer.data)
