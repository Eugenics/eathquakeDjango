import os
import json
import datetime


from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
from django.views import generic
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder


from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session


from .models import Eathquake
from .get_json import get_json_data
from .sql_db import create_row

#----- Auth pages -----------------------------
def loginpage(request):
    if request.method == 'POST':
        user_name = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            request.session['username'] = user_name
            login(request, user)
            return redirect(reverse('home'))
        else:
            context = {
                'error_message': 'login error',
            }
            return render(request, 'login.html', context)
    return render(request, 'login.html')


def profilepage(request):
    if request.session.has_key('username'):
        user_name = request.session['username']
        query = User.objects.filter(username=user_name)
        return render(request, 'profile.html', {"query": query})
    else:
        return render(request, 'login.html', {})


def logoutpage(request):
    try:
        del request.session['username']
    except:
        pass
    return render(request, 'login.html', {})
#----------------------------------------------

@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


class EathquakeSearchView(LoginRequiredMixin, generic.TemplateView):
    template_name = "map.html"

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

        feature_json_list = list(features.values(
            'session_id', 'src', 'id_eathquake', 'version', 'eathquake_time', 'lat', 'lng', 'mag',
            'depth', 'nst', 'region', 'data_source', 'create_date', 'url', 'lat_deg', 'lng_deg'
        ))

        context['session_key'] = session_key
        context['quake_count'] = features.count()
        context['eathquake_features'] = features
        context['date_from'] = date_from
        context['date_till'] = date_till
        context['mag'] = mag
        context['region'] = region
        context['json_list'] = json.dumps(
            feature_json_list, cls=DjangoJSONEncoder)

        return context


@login_required
def mappage(request):
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

    feature_json_list = list(features.values(
        'session_id', 'src', 'id_eathquake', 'version', 'eathquake_time', 'lat', 'lng', 'mag',
        'depth', 'nst', 'region', 'data_source', 'create_date', 'url', 'lat_deg', 'lng_deg'
    ))

    context = {
        'session_key': session_key,
        'quake_count': features.count(),
        'eathquake_features': features,
        'date_from': date_from,
        'date_till': date_till,
        'mag': mag,
        'region': region,
        'json_list': json.dumps(feature_json_list, cls=DjangoJSONEncoder),
    }

    return render(request, 'map.html', context)


# ----------------- AJAX functions -------------------------------------------------------

@login_required
def get_filter_json_data(request):
    date_from = datetime.datetime.now(
        tz=timezone.utc).date().strftime("%Y-%m-%d")
    date_till = datetime.datetime.now(
        tz=timezone.utc).date().strftime("%Y-%m-%d")
    mag = 0
    region = ''

    if 'date_from' in request.GET:
        date_from = request.GET['date_from']

    if 'date_till' in request.GET:
        date_till = request.GET['date_till']

    if 'mag' in request.GET:
        mag = request.GET['mag']

    features = Eathquake.objects.filter(
        mag__gte=mag, eathquake_time__gte=date_from, eathquake_time__lte=date_till)

    # ----------------- Region filter
    if 'region' in request.GET:
        region = request.GET['region']
        if len(region) > 0:
            features = features.filter(region__icontains=region)

    features_list = list(features.values(
        'session_id', 'src', 'id_eathquake', 'version', 'eathquake_time', 'lat', 'lng', 'mag',
        'depth', 'nst', 'region', 'data_source', 'create_date', 'url', 'lat_deg', 'lng_deg')
    )

    return JsonResponse(features_list, safe=False)

# def set_json_string(features, ss_key):
#
#   json_text = '{ "points" : ['
#
#    for feature in features:
#        json_text = json_text + '{ "id":"' + str(feature.id) + '", "Lat":' + str(feature.lat) + ', "Lng": ' + str(feature.lng) + ', "Mag": ' + str(
#            feature.mag) + ', "url": "' + str(feature.url) + '", "Place": "' + str(feature.region) + '", "Time": "' + str(feature.eathquake_time) + '" },'
#
#    json_text = json_text + '{ "id":"empty", "Lat":0, "Lng":0, "Mag":0 }'
#    json_text = json_text + ' ]}'
#
#    return json_text


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
