import datetime, calendar
from django.db import models
from django.utils import timezone

from .calculation import haversine

class Route(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    
    def was_created_today(self):
        return self.creation_date.date() == timezone.now().date() 

    def length(self):
        points = self.point_set.all().values('lat', 'lon')
        count = self.point_set.count()

        total = 0
        idx = 0
        while idx + 1 < count:
            coord1 = points[idx]['lat'], points[idx]['lon']
            coord2 = points[idx + 1]['lat'], points[idx + 1]['lon']
            total += haversine(coord1, coord2)
            idx += 1 
            
        return total

    def __str__(self):
        return "%s" % self.creation_date.strftime("%d/%m/%Y")


class Point(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    lat = models.FloatField(default=0)
    lon = models.FloatField(default=0)

    def __str__(self):
        return "lat: %s, lon: %s" % (self.lat, self.lon)


def get_max(date):
    if date.date() == timezone.now().date():
        return 0
    routes = Route.objects.filter(
                creation_date__day=date.day, 
                creation_date__month=date.month, 
                creation_date__year=date.year)
    if routes:
        return max(map(lambda x: x.length(), routes), default=0)
    return 0

def get_stats(year, month):
    num_days = calendar.monthrange(year, month)[1]
    dates = [datetime.date(year, month, day) for day in range(1, num_days+1)]
    stats = {}
    for date in dates:
        maxx = get_max(date)
        if maxx != 0:
            stats[date] = maxx
    return stats