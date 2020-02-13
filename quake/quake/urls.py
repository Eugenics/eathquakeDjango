from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.conf import settings
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('', views.dashboard, name='home'),    
    path('admin/', admin.site.urls),
    #path('quakemap/', include('quakemap.urls'), name='map'),    
    path('signin/', views.loginpage, name='signin'),
    path('profile/', views.profilepage, name='profile'),
    path('logout/', views.logoutpage, name='logout'),
]


urlpatterns += [
    path('map/', views.mappage, name='map'),
    path('map/search/', views.EathquakeSearchView.as_view(), name='search'),
    path('map/api/quakelist/', views.get_filter_json_data, name='quakelist'),    
]


urlpatterns += [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/update/',views.update_dashboard,name='dashboard_update'),
    path('update/',views.update_dashboard,name='dashboard_update'),
]

