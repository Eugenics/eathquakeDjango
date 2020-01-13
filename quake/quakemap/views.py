from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.sessions.models import Session


def index(request):
    session_key = request.session.session_key
    #cookie_age = request.session.get_session_cookie_age()
    #return HttpResponse('Session key: ' + session_key)

    context = {
        'session_key':session_key,
    }

    return render(request,'index.html',context)
