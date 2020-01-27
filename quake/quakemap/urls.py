from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.EathquakeSearchView.as_view(), name='search'),
    path('srch/', views.get_json_text, name='srch'),
]
