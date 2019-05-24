from typing import Union

from config.static_values import END_TIME_PENALTY
from log_book.application.abc_processor import ABCStreamProcessor
from log_book.models.models import Trip, WayPoint, TripEntity
from log_book.util.haversine import distance as haversine_distance


class StreamProcessor(ABCStreamProcessor):

    def __init__(self):
        super().__init__()
        self.trip = TripEntity()
        self.way_points = []
        self.last_time_moved = None

    def update_distance(self):
        self.trip.distance += haversine_distance(self.way_points[-2], self.way_points[-1])
        self.last_time_moved = self.way_points[-1].timestamp

    def flush(self):
        self.trip = TripEntity()
        self.way_points = self.way_points[-1:]
        self.last_time_moved = None

    def process_waypoint(self, waypoint: WayPoint) -> Union[Trip, None]:
        if isinstance(self.trip.end, WayPoint):
            self.flush()

        if len(self.way_points) == 0:
            self.way_points.append(waypoint)

        if waypoint == self.way_points[-1]:
            if len(self.way_points) > 1 and \
                                    waypoint.timestamp - self.last_time_moved > END_TIME_PENALTY:
                self.trip.end = self.way_points[-1]
                return Trip(start=self.trip.start, end=self.trip.end, distance=self.trip.distance)

            self.way_points[-1] = waypoint

        else:
            if self.trip.start is None:
                self.trip.start = self.way_points[-1]

            self.way_points.append(waypoint)
            self.update_distance()
        return None

