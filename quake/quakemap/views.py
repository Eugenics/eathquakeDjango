from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from .models import Eathquake
from .get_json import get_json_data


def index(request):
    session_key = request.session.session_key
    
    eathquake_features = get_json_data("2020-01-13","2020-01-14")
    

    context = {
        'session_key':session_key,
        'eathquake_features':eathquake_features,
    }

    return render(request,'index.html',context)
