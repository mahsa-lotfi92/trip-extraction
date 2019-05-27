from typing import Union

from log_book.application.abc_processor import ABCStreamProcessor
from log_book.config.static_values import MAX_TIME_WITHOUT_MOVEMENT, MAX_ACCEPTABLE_VELOCITY
from log_book.models.models import Trip, WayPoint
from log_book.util.haversine import distance as haversine_distance
from log_book.util.misc import TripEntity


class StreamProcessor(ABCStreamProcessor):

    def __init__(self):
        super().__init__()
        self.trip = TripEntity()
        self.way_points = []
        self.last_time_updated = None

    def get_last_velocity(self, way_point: WayPoint):
        time_passed = (way_point.timestamp-self.way_points[-1].timestamp).seconds
        return haversine_distance(self.way_points[-1], way_point) / time_passed if time_passed > 0 else 0

    def update_distance(self):
        self.trip.distance += haversine_distance(self.way_points[-2], self.way_points[-1])

    def flush(self):
        self.trip = TripEntity()
        self.way_points = self.way_points[-1:]
        self.last_time_updated = None

    def process_waypoint(self, waypoint: WayPoint) -> Union[Trip, None]:
        if not isinstance(waypoint, WayPoint):
            return None

        if isinstance(self.trip.end, WayPoint):
            self.flush()

        if len(self.way_points) == 0:
            self.way_points.append(waypoint)

        elif self.get_last_velocity(waypoint) > MAX_ACCEPTABLE_VELOCITY:
            pass

        elif waypoint.is_near(self.way_points[-1]):
            if len(self.way_points) > 1 and \
                                    waypoint.timestamp - self.way_points[-1].timestamp > MAX_TIME_WITHOUT_MOVEMENT:
                self.trip.end = self.way_points[-1]
                return self.trip.to_trip()
        else:
            if self.trip.start is None:
                self.trip.start = WayPoint(lat=self.way_points[-1].lat,
                                           lng=self.way_points[-1].lng,
                                           timestamp=self.last_time_updated)

            self.way_points.append(waypoint)
            self.update_distance()

        self.last_time_updated = waypoint.timestamp
        return None

