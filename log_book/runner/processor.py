from log_book.application.stream_processor import StreamProcessor
from log_book.models.models import WayPoint


def process_waypoints(waypoints):
    processor = StreamProcessor()
    trips = []
    for waypoint in waypoints:
        waypoint = WayPoint.create_from_dict(obj=waypoint)
        trip = processor.process_waypoint(waypoint)
        if trip:
            trips.append(trip.to_dict())
    return trips

