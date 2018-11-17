from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import mixins

from datachimp.models.data import Data
from datachimp.serializers.data import DataSerializer

from datachimp.api_permissions import HasProjectMembership
from rest_framework.permissions import IsAuthenticated


class CreateDataVersionAPI(mixins.CreateModelMixin,
                           viewsets.GenericViewSet):
    serializer_class = DataSerializer
    queryset = Data.objects.all()
    permission_classes = (IsAuthenticated, HasProjectMembership)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
