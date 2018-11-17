from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import mixins
from django.http import HttpResponse

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


class RetrieveDataVersionAPI(mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    serializer_class = DataSerializer
    queryset = Data.objects.all()
    permission_classes = (IsAuthenticated, HasProjectMembership)

    def retrieve(self, request, *args, **kwargs):
        try:
            # Get the filter parameters from the request
            params = self.request.query_params
            data_version = None

            # Check if the duration exists
            if 'data-version' in params:
                data_version = params['data-version']
            else:
                raise Exception("data-version required")
        except Exception as e:
            return Response("Error: %s" % e, status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_queryset().get(version_id=data_version)

        files_path_pointer = instance.files_path
        response = HttpResponse(files_path_pointer,content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=NameOfFile'

        return response
