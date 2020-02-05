from django.urls import path
from . import views



urlpatterns = [
    path('map/', views.mappage, name='map'),
    path('map/search/', views.EathquakeSearchView.as_view(), name='search'),
    path('map/api/quakelist/', views.get_filter_json_data, name='quakelist'),    
] 
