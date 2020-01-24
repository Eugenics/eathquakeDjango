from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from .models import Eathquake
from .get_json import get_json_data
from .sql_db import create_row
import os
import datetime
from django.views import generic
import json
from django.utils import timezone


class EathquakeSearchView(generic.TemplateView):
    template_name = "index.html"

    def get_queryset(self):
        return Eathquake.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        session_key = self.request.session.session_key

        feature_list = Eathquake.objects.all()

        date_from = datetime.datetime.now(
            tz=timezone.utc).date().strftime("%Y-%m-%d")
        date_till = datetime.datetime.now(
            tz=timezone.utc).date().strftime("%Y-%m-%d")
        mag = 0
        region = ''

        if 'date_from' in self.request.GET:
            date_from = self.request.GET['date_from']

        if 'date_till' in self.request.GET:
            date_till = self.request.GET['date_till']

        if 'mag' in self.request.GET:
            mag = self.request.GET['mag']

        eathquakes_list = get_json_data(date_from, date_till)
        eathquake_features = eathquakes_list["features"]

        for feature in eathquake_features:
            if feature_list.filter(id_eathquake=feature['id']).count() == 0:
                create_row(feature, session_key)

        features = feature_list

        # ----------------- Region filter
        if 'region' in self.request.GET:
            region = self.request.GET['region']
            if len(region) > 0:
                features = features.filter(region__icontains=region)

        features = features.filter(
            mag__gte=mag, eathquake_time__gte=date_from, eathquake_time__lte=date_till)

        json_text = set_json_string(features, session_key)

        context['session_key'] = session_key
        context['quake_count'] = features.count()
        context['eathquake_features'] = features
        context['date_from'] = date_from
        context['date_till'] = date_till
        context['mag'] = mag
        context['region'] = region
        context['json_text'] = json_text

        return context


def index(request):
    session_key = request.session.session_key

    day = datetime.timedelta(days=1)

    date_from = datetime.datetime.now()  # - day
    date_from = date_from.strftime("%Y-%m-%d")
    date_till = datetime.datetime.now() + day
    date_till = date_till.strftime("%Y-%m-%d")

    mag = 0
    region = ''

    eathquakes_list = get_json_data(date_from, date_till)
    eathquake_features = eathquakes_list["features"]
    feature_list = Eathquake.objects.all()

    for feature in eathquake_features:
        if feature_list.filter(id_eathquake=feature['id']).count() == 0:
            create_row(feature, session_key)

    features = Eathquake.objects.filter(
        mag__gte=mag, eathquake_time__gte=date_from, eathquake_time__lte=date_till)

    json_text = set_json_string(features, session_key)

    context = {
        'session_key': session_key,
        'quake_count': features.count(),
        'eathquake_features': features,
        'date_from': date_from,
        'date_till': date_till,
        'mag': mag,
        'region': region,
        'json_text': json_text,
    }

    return render(request, 'index.html', context)


def search(request, date_from, date_till, mag, region):
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


def set_json_string(features, ss_key):

    json_text = '{ "points" : ['

    for feature in features:
        json_text = json_text + '{ "id":"' + str(feature.id) + '", "Lat":' + str(feature.lat) + ', "Lng": ' + str(feature.lng) + ', "Mag": ' + str(
            feature.mag) + ', "url": "' + str(feature.url) + '", "Place": "' + str(feature.region) + '", "Time": "' + str(feature.eathquake_time) + '" },'

    json_text = json_text + '{ "id":"empty", "Lat":0, "Lng":0, "Mag":0 }'
    json_text = json_text + ' ]}'

    return json_text


def get_json_text():
    feature_list = Eathquake.objects.all()
    session_key = ""

    date_from = '2020-01-24'
    date_till = '2020-01-25'

    mag = 0
    region = ''

    #if 'mag' in self.request.GET:
    #    mag = self.request.GET['mag']

    #eathquakes_list = get_json_data(date_from, date_till)
    #eathquake_features = eathquakes_list["features"]

    #for feature in eathquake_features:
    #    if feature_list.filter(id_eathquake=feature['id']).count() == 0:
    #        create_row(feature, session_key)

    features = feature_list

    # ----------------- Region filter
    #if 'region' in self.request.GET:
    #    region = self.request.GET['region']
    #    if len(region) > 0:
    #        features = features.filter(region__icontains=region)

    features = features.filter(
        mag__gte=mag, eathquake_time__gte=date_from, eathquake_time__lte=date_till)

    json_text = set_json_string(features, session_key)

    return json_text
