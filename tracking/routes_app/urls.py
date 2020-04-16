from django.urls import path
from . import views

app_name = 'routes_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:route_id>/length/', views.length, name='length'),
    path('<int:route_id>/way_point', views.way_point, name='way_point'),
    path('statistics', views.statistics, name='statistics')
]