from rest_framework import serializers

from .models import Route, Point


class PointSerializer(serializers.ModelSerializer):

    class Meta:
        model = Point
        fields = ('lat', 'lon',)


class RouteListPageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        exclude = ()


class RouteDetailPageSerializer(RouteListPageSerializer):
    points = PointSerializer(many=True, read_only=True)


class LengthSerializer(serializers.Serializer):
    length = serializers.FloatField()
