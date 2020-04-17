from django.urls import path
from . import views, apiviews

app_name = 'routes_app'
urlpatterns = [
    path('old_style', views.index, name='index'),
    path('old_style/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('old_style/<int:route_id>/length/', views.length, name='length'),
    path('old_style/<int:route_id>/way_point/', views.way_point, name='way_point'),
    path('old_style/statistics/', views.statistics, name='statistics'),

    path('', apiviews.routes_view, name='routes_view'),
    path('<int:route_id>/', apiviews.route_detail_view, name='route_detail_view'),
    path('<int:route_id>/way_point/', apiviews.points_view, name='points_view'),
    path('<int:route_id>/length/', apiviews.length_view, name='length_view'),
]