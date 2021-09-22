from django.contrib.auth.models import User, Group
from rest_framework import views, viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer, MsectionSerializer, \
    MpointSerializer, MvalueSerializer
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from .models import Msections, Mpoint, Mvalue
from django_filters.rest_framework import DjangoFilterBackend


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class MsectionViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    Be able to query all the sections
    '''
    queryset = Msections.objects.all()
    serializer_class = MsectionSerializer


class MpointViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    Be able to query all the sections
    '''
    queryset = Mpoint.objects.all()
    serializer_class = MpointSerializer
    filterset_fields = ['section__name']
    filter_backends = [DjangoFilterBackend]


class MvalueViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    Be able to query all the sections
    '''
    queryset = Mvalue.objects.all()
    serializer_class = MvalueSerializer
    filterset_fields = ['m_point__name']
    filter_backends = [DjangoFilterBackend]
