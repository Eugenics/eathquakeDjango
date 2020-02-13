import os
import json
import datetime


from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
from django.views import generic
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Max, FloatField


from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session


from .models import Eathquake
from .get_json import get_json_data
from .sql_db import create_row

# ----- Auth pages -----------------------------


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
# ----------------------------------------------


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def dashboard(request):
    max_data = get_data_for_dashboard(request)
    context = {
        'chart_day_data': max_data['chart_day_data'],
        'chart_mon_data': max_data['chart_mon_data'],
        'chart_max_data': max_data['chart_max_data'],
        'date_from': max_data['date_from'],
        'date_till': max_data['date_till'],
        'session_key': max_data['session_key'],
    }
    return render(request, 'dashboard.html', context)


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

# ----------------- Functions ------------------------------------------------------------


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


def update_db_data(date_from, date_till, session_key):
    """[Function for update data in database]

    Arguments:
        date_from {[date time]} -- [Date from]
        date_till {[date time]} -- [Date till]
        session_key {[type]} -- [Session key]
    """

    eathquakes_list = get_json_data(date_from, date_till)
    eathquake_features = eathquakes_list["features"]

    for feature in eathquake_features:
        if Eathquake.objects.filter(id_eathquake=feature['id']).count() == 0:
            create_row(feature, session_key)


def get_data_for_dashboard(request):
    session_key = request.session.session_key

    day = datetime.timedelta(days=1)

    date_from = datetime.datetime.now()  # - day
    date_from = date_from.strftime("%Y-%m-%d")
    date_till = datetime.datetime.now() + day
    date_till = date_till.strftime("%Y-%m-%d")

    update_db_data(date_from, date_till, session_key)

    first_day_of_month = datetime.datetime.now().strftime("%Y-%m-01")
    first_day_of_year = datetime.datetime.now().strftime("%Y-01-01")

    # Total in past day
    mag_less_3 = Eathquake.objects.filter(
        mag__lt=3, eathquake_time__gte=date_from, eathquake_time__lte=date_till).count()
    mag_less_6 = Eathquake.objects.filter(
        mag__lt=6, mag__gte=3, eathquake_time__gte=date_from, eathquake_time__lte=date_till).count()
    mag_more_6 = Eathquake.objects.filter(
        mag__gte=6, eathquake_time__gte=date_from, eathquake_time__lte=date_till).count()

    # Total in current month
    mag_mon_less_3 = Eathquake.objects.filter(
        mag__lt=3, eathquake_time__gte=first_day_of_month, eathquake_time__lte=date_till).count()
    mag_mon_less_6 = Eathquake.objects.filter(
        mag__lt=6, mag__gte=3, eathquake_time__gte=first_day_of_month, eathquake_time__lte=date_till).count()
    mag_mon_more_6 = Eathquake.objects.filter(
        mag__gte=6, eathquake_time__gte=first_day_of_month, eathquake_time__lte=date_till).count()

    # Max mag in past day
    max_day_mag = Eathquake.objects.filter(
        eathquake_time__gte=date_from, eathquake_time__lte=date_till
    ).aggregate(Max('mag', output_field=FloatField()))
    # Max mag in current manth
    max_mon_mag = Eathquake.objects.filter(
        eathquake_time__gte=first_day_of_month, eathquake_time__lte=date_till
    ).aggregate(Max('mag', output_field=FloatField()))
    # Max mag in current year
    max_year_mag = Eathquake.objects.filter(
        eathquake_time__gte=first_day_of_year, eathquake_time__lte=date_till
    ).aggregate(Max('mag', output_field=FloatField()))

    return {
        "date_from": date_from,
        "date_till": date_till,
        "session_key": session_key,
        "chart_day_data": {"mag_3": mag_less_3,
                            "mag_4": mag_less_6, "mag_6": mag_more_6},
        "chart_mon_data": {"mag_3": mag_mon_less_3,
                            "mag_4": mag_mon_less_6, "mag_6": mag_mon_more_6},
        "chart_max_data": {
            "max_day": max_day_mag['mag__max'],
            "max_mon": max_mon_mag['mag__max'],
            "max_year": max_year_mag['mag__max'],
        },
    }

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


@login_required
def update_dashboard(request):
    return JsonResponse(get_data_for_dashboard(request), safe=False)