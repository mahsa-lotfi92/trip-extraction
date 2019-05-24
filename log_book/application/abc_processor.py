from abc import ABCMeta, abstractmethod
from typing import Union
from log_book.models.models import Trip, WayPoint


class ABCStreamProcessor(metaclass=ABCMeta):

    def __init__(self):
        pass

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
