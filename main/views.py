from rest_framework import viewsets
from .serializers import MsectionSerializer, \
    MpointSerializer, MvalueSerializer
from .models import Msections, Mpoint, Mvalue
from django_filters.rest_framework import DjangoFilterBackend


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

    def get_queryset(self):
        points = self.request.GET.get('m_points', '')
        if points:
            points_values = points.split(',')
            return Mvalue.objects.filter(m_point__name__in=points_values)
        return Mvalue.objects.all()
