from rest_framework import serializers
from .models import Msections, Mpoint, Mvalue


class MsectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Msections
        fields = ['url', 'name']


class MpointSerializer(serializers.HyperlinkedModelSerializer):
    section_name = serializers.CharField(source='section.name')

    class Meta:
        model = Mpoint
        fields = ['url', 'name', 'section_name', 'section']


class MvalueSerializer(serializers.HyperlinkedModelSerializer):
    point_name = serializers.CharField(source='m_point.name')
    
    class Meta:
        model = Mvalue
        fields = ['url', 'value', 'point_name', 'm_point', 'm_time']
