from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from .models import Eathquake
from .get_json import get_json_data
from .sql_db import create_row
import os
import datetime
from django.views import generic


class EathquakeSearchView(generic.TemplateView):
    template_name = "index.html"

    def get_queryset(self):
        return Eathquake.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        session_key = self.request.session.session_key

        feature_list = Eathquake.objects.all()


        date_from = datetime.datetime.now().date().strftime("%Y-%m-%d")
        date_till = datetime.datetime.now().date().strftime("%Y-%m-%d")
        mag = 0

        if 'date_from' in self.request.GET:
            date_from = self.request.GET['date_from']
            
        if 'date_till' in self.request.GET:
            date_till = self.request.GET['date_till']

        if 'mag' in self.request.GET:
            mag = self.request.GET['mag']

        eathquake_features = get_json_data(date_from, date_till)

        for feature in eathquake_features:
            if feature_list.filter(id_eathquake=feature['id']).count() == 0:
                create_row(feature, session_key)

        features = Eathquake.objects.filter(
            mag__gte=mag, eathquake_time__gte=date_from, eathquake_time__lte=date_till)

        context['session_key'] = session_key
        context['quake_count'] = features.count()
        context['eathquake_features'] = features
        context['date_from'] = date_from
        context['date_till'] = date_till
        context['mag'] = mag

        return context


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


def search(request, date_from, date_till, mag):
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
