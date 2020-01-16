from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from .models import Eathquake
from .get_json import get_json_data
from .sql_db import create_row
import os
import datetime


def index(request):
    session_key = request.session.session_key
    feature_list = Eathquake.objects.all()

    date_from = datetime.datetime.now().date().strftime("%Y-%m-%d")
    date_till = datetime.datetime.now().date().strftime("%Y-%m-%d")

    #date_from = date_from - datetime.timedelta(days=1)

    mag = 5.0

    eathquake_features = get_json_data(date_from, date_till)

    for feature in eathquake_features:
        if feature_list.filter(id_eathquake=feature['id']).count() == 0:
            create_row(feature, session_key)

    features = Eathquake.objects.filter(mag=mag)

    context = {
        'session_key': session_key,
        'quake_count': features.count(),
        'eathquake_features': features,
        'date_from': date_from,
        'date_till': date_till,
        'mag': mag,
    }

    return render(request, 'index.html', context)


def search(date_from, date_till, mag):
    session_key = request.session.session_key
    feature_list = Eathquake.objects.all()

    date_from = datetime.datetime.now().date().strftime("%Y-%m-%d")
    date_till = datetime.datetime.now().date().strftime("%Y-%m-%d")    

    context = {
        'session_key': session_key,
        'quake_count': feature_list.count(),
        'eathquake_features': feature_list,
        'date_from': date_from,
        'date_till': date_till,
        'mag': mag,
    }
    return render(request, 'index.html', context)
