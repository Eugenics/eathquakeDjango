from django.db import models
from decimal import Decimal


class Eathquake(models.Model):
    session_id = models.UUIDField()    
    src = models.CharField(max_length=50)
    id_eathquake = models.CharField(max_length=50)
    version = models.CharField(max_length=50)
    eathquake_time = models.DateTimeField()
    lat = models.DecimalField(max_digits=18,decimal_places=6)
    lng = models.DecimalField(max_digits=18,decimal_places=6)
    mag = models.DecimalField(max_digits=18,decimal_places=6)
    depth = models.DecimalField(max_digits=18,decimal_places=6)
    nst = models.CharField(max_length=50)
    region = models.CharField(max_length=2500)
    data_source = models.CharField(max_length=500)
    create_date = models.DateTimeField()
