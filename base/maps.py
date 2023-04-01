import googlemaps
from datetime import datetime
from .keys import *

def get_directions(origin, destination):
    gmaps = googlemaps.Client(key=MAPS_KEY)
    now = datetime.now()
    directions_result = gmaps.directions(origin,
                                         destination,
                                         mode="driving",
                                         departure_time=now)
    
    return directions_result
