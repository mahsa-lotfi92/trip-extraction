from datetime import datetime
from typing import NamedTuple

from config.static_values import IGNORE_DISTANCE
from util.haversine import distance as haversine_distance


class WayPoint(NamedTuple):
    timestamp: datetime
    lat: float
    lng: float

    def __eq__(self, waypoint2) -> bool:
        assert isinstance(waypoint2, WayPoint)
        return haversine_distance(self, waypoint2) <= IGNORE_DISTANCE


class Trip(NamedTuple):
    distance: int
    start: WayPoint
    end: WayPoint