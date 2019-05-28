from typing import List

from log_book.application.stream_processor import StreamProcessor
from log_book.models.models import WayPoint


def process_way_points(way_points: List[WayPoint]):
    processor = StreamProcessor()
    trips = []
    for way_point in way_points:
        way_point = WayPoint.create_from_dict(obj=way_point)
        trip = processor.process_waypoint(way_point)
        if trip:
            trips.append(trip.to_dict())
    return trips

