from math import sin, cos, sqrt, radians, asin


# https://en.wikipedia.org/wiki/Haversine_formula
def haversine(coord1, coord2):
    R = 6372.89 #km
    lat1, lon1 = coord1
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2, lon2 = coord2
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    return 2*R*asin(sqrt(sin((lat2 - lat1)/2)**2 + cos(lat1)*cos(lat2)*sin((lon2 - lon1)/2)**2))
    