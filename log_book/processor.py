from abc import ABCMeta, abstractmethod
from typing import Union

from config.static_values import END_TIME_PENALTY
from log_book.models import Trip, WayPoint
from util.haversine import distance as haversine_distance


class StreamProcessor(metaclass=ABCMeta):

    def __init__(self):
        self.trip = Trip(distance=0, start=None, end=None)
        self.way_points = []
        self.last_time_received_location = None

    def update_distance(self):
        self.trip.distance += haversine_distance(self.way_points[-2], self.way_points[-1])

    def flush(self):
        self.__init__()

    @abstractmethod
    def process_waypoint(self, waypoint: WayPoint) -> Union[Trip, None]:
        """
        Instead of a list of Waypoints, the StreamProcessor only receives one
        Waypoint at a time. The processor does not have access to the full list
        of waypoints.
        If the stream processor recognizes a complete trip, the processor
        returns a Trip object, otherwise it returns None.

        :param waypoint: Waypoint
        """
        ...
        if waypoint == self.way_points[-1]:
            if waypoint.timestamp - self.way_points[-1].timestamp > END_TIME_PENALTY and \
                    len(self.way_points) > 1:
                self.trip.end = self.way_points[-1]
                return self.trip

            self.last_time_received_location = waypoint.timestamp
            return None
        else:
            if self.trip.start is None:
                self.trip.start = self.way_points[-1]
                self.trip.start.timestamp = self.last_time_received_location

            self.way_points.append(waypoint)
            self.update_distance()
            self.last_time_received_location = waypoint.timestamp

