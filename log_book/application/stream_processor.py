from typing import Union

from log_book.application.abc_processor import ABCStreamProcessor
from log_book.config.static_values import MAX_TIME_WITHOUT_MOVEMENT, MAX_ACCEPTABLE_VELOCITY
from log_book.models.models import Trip, WayPoint
from log_book.util.haversine import distance as haversine_distance
from log_book.util.misc_models import TripEntity


class StreamProcessor(ABCStreamProcessor):

    def __init__(self):
        super().__init__()
        self.trip = TripEntity()
        self.last_way_point = None
        self.last_time_updated = None

    def get_last_velocity(self, way_point: WayPoint):
        return WayPoint.get_velocity(self.last_way_point, way_point)

    def update_distance(self, new_waypoint: WayPoint):
        self.trip.distance += haversine_distance(self.last_way_point, new_waypoint)

    def flush(self):
        self.trip = TripEntity()
        self.last_time_updated = None

    def process_waypoint(self, waypoint: WayPoint) -> Union[Trip, None]:
        if not isinstance(waypoint, WayPoint):
            return None

        if self.trip.end is not None:
            self.flush()

        if self.last_way_point is None:
            self.last_way_point = waypoint

        elif self.get_last_velocity(waypoint) > MAX_ACCEPTABLE_VELOCITY:
            # to handle jumps in received locations we skip the points that cause
            # the movement pace more than 30 meter per second
            pass

        elif waypoint.is_near(self.last_way_point):
            # if the points are close to each other less than 15 meters, the new point should not be count as movement
            # and if there is more than 3 minutes that vehicle did not move, the trip should be ended.
            if self.trip.start is not None and \
                                    waypoint.timestamp - self.last_way_point.timestamp > MAX_TIME_WITHOUT_MOVEMENT:
                self.trip.end = self.last_way_point
                return self.trip.to_trip()
        else:
            if self.trip.start is None:
                self.trip.start = WayPoint(lat=self.last_way_point.lat,
                                           lng=self.last_way_point.lng,
                                           timestamp=self.last_time_updated)
                # to handle the start time of the trip should as soon as the vehicle moves

            self.update_distance(waypoint)
            self.last_way_point = waypoint

        self.last_time_updated = waypoint.timestamp
        return None

