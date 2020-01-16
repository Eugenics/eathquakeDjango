from django.db import models
from django.urls import reverse_lazy, reverse
from decimal import Decimal


class Eathquake(models.Model):
    session_id = models.CharField(max_length=50)
    src = models.CharField(max_length=50, null=True, blank=True)
    id_eathquake = models.CharField(max_length=50, null=True, blank=True)
    version = models.CharField(max_length=50, null=True, blank=True)
    eathquake_time = models.DateTimeField(null=True, blank=True)
    lat = models.DecimalField(
        max_digits=18, decimal_places=6, null=True, blank=True)
    lng = models.DecimalField(
        max_digits=18, decimal_places=6, null=True, blank=True)
    mag = models.DecimalField(
        max_digits=18, decimal_places=6, null=True, blank=True)
    depth = models.DecimalField(
        max_digits=18, decimal_places=6, null=True, blank=True)
    nst = models.CharField(max_length=50, null=True, blank=True)
    region = models.CharField(max_length=2500, null=True, blank=True)
    data_source = models.CharField(max_length=500, null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    url = models.CharField(max_length=2500,null=True,blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ['eathquake_time']
