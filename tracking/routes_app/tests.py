import datetime

from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Route, Point, get_max

class RouteModelTests(TestCase):

    def test_was_created_today(self):
        route = Route()
        route.save()
        self.assertTrue(route.was_created_today())

    def test_change_created_date(self):
        route = Route()
        route.save()
        route.creation_date = timezone.now() - datetime.timedelta(3)
        route.save()    
        self.assertFalse(route.was_created_today())

    def test_add_points_to_route(self):
        route = Route()
        route.save()
        Point(route=route, lat=3, lon=4).save()
        self.assertIs(route.point_set.count(), 1)

    def test_get_length(self):
        route = Route()
        route.save()
        Point(route=route, lat=52.5170365, lon=13.3888599).save()
        Point(route=route, lat=48.2083537, lon=16.3725042).save()
        length = route.length()
        self.assertTrue(523 < length['vincenty'] < 525)
        self.assertTrue(523 < length['haversine'] < 525)
        self.assertTrue(523 < length['from_pyproj'] < 525)

    def test_get_maximum(self):
        past_date = timezone.now() - datetime.timedelta(3)
        route = Route()
        route.save()
        route.creation_date = past_date 
        route.save()
        Point(route=route, lat=52.5170365, lon=13.3888599).save()
        Point(route=route, lat=48.2083537, lon=16.3725042).save()
        route1 = Route()
        route1.save()
        route1.creation_date = past_date
        route1.save()
        Point(route=route1, lat=52.5170365, lon=13.3888599).save()
        self.assertTrue(523 < get_max(past_date) < 525)


class RouteIndexViewTests(TestCase):
    def test_no_routes(self):
        """
        If no routes exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('routes_app:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No routes are available.")


    def test_one_route(self):
        """
        If one route exists, it should be displayed
        """
        route = Route()
        route.save()
        response = self.client.get(reverse('routes_app:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(route))

