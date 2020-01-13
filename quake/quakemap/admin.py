from django.contrib import admin
from .models import Eathquake
from django.contrib.sessions.models import Session


admin.site.register(Eathquake)


admin.site.register(Session)
