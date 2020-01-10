from django.db import models

# Create your models here.

class Eathquake(models.Model):
    id_info = models.IntegerField()
    src = models.CharField(max_length=50)
    id_eathquake = models.CharField(max_length=50)  
    version = models.CharField(max_length=50)
    eathquake_time = models.DateTimeField()
    lat = models.FloatField()
    lng = models.FloatField()
    mag = models.FloatField()
    depth = models.FloatField()
    nst = models.CharField(max_length=50)
    region = models.CharField(max_legth=2500)
    data_source = models.CharField(max_legth=500)
    create_date = models.DateTimeField()
