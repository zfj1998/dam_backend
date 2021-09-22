from django.db import models


class Msections(models.Model):
    '''截面'''
    name = models.CharField(max_length=64)


class Mpoint(models.Model):
    '''测点'''
    name = models.CharField(max_length=64)
    section = models.ForeignKey(Msections, on_delete=models.CASCADE)


class Mvalue(models.Model):
    '''检测值'''
    value = models.FloatField()
    m_time = models.DateTimeField()
    m_point = models.ForeignKey(Mpoint, on_delete=models.CASCADE)
