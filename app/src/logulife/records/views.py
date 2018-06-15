from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from .models import Record
from .serializers import RecordSerializer, RecordCreateSerializer


class Records(GenericAPIView):

    serializer_class = RecordSerializer

    def get(self, request):

        records = Record.objects.filter(owner=request.user)
        serializer = self.get_serializer(records, many=True)

        return Response(serializer.data)

    def post(self, request):

        self.serializer_class = RecordCreateSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_serializer = RecordSerializer(serializer.instance)

        return Response(response_serializer.data)
