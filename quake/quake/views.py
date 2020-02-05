from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required


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


@login_required
def index(request):
    return render(request, 'index.html')
