from tviit.models import Tviit
from tviit.serializers import TviitSerializer
from tviit.permissions import IsSender
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })

class TviitList(generics.ListCreateAPIView):
    queryset = Tviit.objects.all()
    serializer_class = TviitSerializer

class TviitDetail(APIView):
    permission_classes = (IsSender,)
    def get_object(self, uuid):
        try:
            return Tviit.objects.get(uuid=uuid)
        except Tviit.DoesNotExist:
            raise Http404

    def get(self, request, uuid, format=None):
        tviit = self.get_object(uuid)
        serializer = TviitSerializer(tviit)
        return Response(serializer.data)

    def put(self, request, uuid, format=None):
        tviit = self.get_object(uuid)
        serializer = TviitSerializer(tviit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid, format=None):
        tviit = self.get_object(uuid)
        tviit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)