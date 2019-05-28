from datetime import datetime
from typing import NamedTuple, Dict

from log_book.config.static_values import IGNORE_DISTANCE
from log_book.util.haversine import distance as haversine_distance

TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
class WayPoint(NamedTuple):
    timestamp: datetime
    lat: float
    lng: float

    @staticmethod
    def create_from_dict(obj: Dict):
        if not isinstance(obj, dict):
            raise Exception('Waypoint can be created from dict.')

        lat = obj['lat']
        lng = obj['lng']
        timestamp = datetime.strptime(obj['timestamp'], TIME_FORMAT)
        return WayPoint(timestamp=timestamp, lat=lat, lng=lng)

    @staticmethod
    def get_velocity(start, end) -> float:
        time_passed = (end.timestamp - start.timestamp).seconds
        return haversine_distance(start, end) / time_passed if time_passed > 0 else 0

    def is_near(self, waypoint2) -> bool:
        assert isinstance(waypoint2, WayPoint)
        return haversine_distance(self, waypoint2) <= IGNORE_DISTANCE

    def __repr__(self):
        return '(lat:{}, lng:{}, time:{})'.format(self.lat, self.lng, self.timestamp)

    def __eq__(self, other):
        return self.lat == other.lat and self.lng == other.lng and self.timestamp == other.timestamp

    def to_dict(self):
        return {'timestamp': self.timestamp,
                'lat': self.lat,
                'lng': self.lng}


class Trip(NamedTuple):
    distance: int
    start: WayPoint
    end: WayPoint

    def to_dict(self):
        return {'distance': self.distance,
                'start': self.start.to_dict(),
                'end': self.end.to_dict()}
