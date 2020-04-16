from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.views import generic

import datetime, calendar

from .models import Route, Point, get_stats


class DetailView(generic.DetailView):
    model = Route
    template_name = 'routes_app/detail.html'

def index(request):
    if request.POST:
        route = Route()
        route.save()
    
    routes = Route.objects.all()
    context = {}
    if routes:
        context['routes'] = routes
    return render(request, 'routes_app/index.html', context)

def length(request, route_id):
    route = get_object_or_404(Route, pk=route_id)
    context = {
        'route': route , 
        'length': route.length()
    }
    return render(request, 'routes_app/detail.html', context)

def way_point(request, route_id):
    route = get_object_or_404(Route, pk=route_id)
    lat = request.POST['lat']
    lon = request.POST['lon']

    if route.was_created_today():
        point = Point(route=route, lat=lat, lon=lon)
        point.save()
    return render(request, 'routes_app/detail.html', {'route': route})

def statistics(request):
    year = int(request.POST['year'])
    month = int(request.POST['month'])
    stats = get_stats(year, month)
    return render(request, 'routes_app/stats.html', {'stats': stats})