from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Route, Point
from .serializers import RouteListPageSerializer, RouteDetailPageSerializer, PointSerializer, LengthSerializer


@api_view(['GET', 'POST'])
def routes_view(request):
    if request.method == 'GET':
        routes = Route.objects.all()
        serializer = RouteListPageSerializer(routes, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RouteListPageSerializer(data=request.data)
        if serializer.is_valid():
            route = Route.objects.create()
            content = {'route_id': route.id}
            return Response(content, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
def route_detail_view(request, route_id):
    route = get_object_or_404(Route, pk=route_id)
    if request.method == 'GET':
        serializer = RouteDetailPageSerializer(route)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = RouteDetailPageSerializer(route, data=request.data, partial=True)
        if serializer.is_valid():
            route = serializer.save()
            return Response(RouteDetailPageSerializer(route).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        route.delete()
        return Response("Route deleted", status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def points_view(request, route_id):
    route = get_object_or_404(Route, pk=route_id)
    if request.method == 'GET':
        points = route.point_set.all()
        serializer = PointSerializer(points, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PointSerializer(data=request.data)
        if serializer.is_valid():
            point = serializer.save(route=route)
            return Response(PointSerializer(point).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def length_view(request, route_id):
    route = get_object_or_404(Route, pk=route_id)
    length = route.length()
    content = {'km': length}
    return Response(content)