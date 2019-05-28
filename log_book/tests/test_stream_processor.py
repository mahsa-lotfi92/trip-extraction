import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock

from log_book.application.stream_processor import StreamProcessor
from log_book.models.models import WayPoint


class StreamProcessorTest(unittest.TestCase):
    @patch('log_book.application.stream_processor.StreamProcessor.process_waypoint', new_callable=MagicMock)
    @patch('log_book.models.models.haversine_distance', new_callable=MagicMock)
    def test_get_last_velocity(self, haversine_distance_mock, process_waypint_mock):
        uut = StreamProcessor()

        def haversine_distance(p1, p2):
            if p1.lat == p2.lat and p1.lng == p2.lng:
                return 0
            return 20

        def process_waypoint(waypoint):
            uut.last_way_point = waypoint
            return

        process_waypint_mock.side_effect = process_waypoint
        haversine_distance_mock.side_effect = haversine_distance

        def run():
            p1 = WayPoint(lat=1, lng=1, timestamp=datetime(year=2019, month=12, day=12))
            p2 = WayPoint(lat=1, lng=1, timestamp=datetime(year=2019, month=12, day=12, second=20))
            p3 = WayPoint(lat=1, lng=1, timestamp=datetime(year=2019, month=12, day=12, second=40))
            p4 = WayPoint(lat=2, lng=2, timestamp=datetime(year=2019, month=12, day=12, second=40))
            p5 = WayPoint(lat=3, lng=3, timestamp=datetime(year=2019, month=12, day=12, second=50))

            uut.process_waypoint(p1)
            result = uut.get_last_velocity(p1)
            expected = 0
            self.assertEqual(expected, result)

            uut.process_waypoint(p2)
            result = uut.get_last_velocity(p3)
            expected = 0
            self.assertEqual(expected, result)

            uut.process_waypoint(p3)
            result = uut.get_last_velocity(p4)
            expected = 0
            self.assertEqual(expected, result)

            uut.process_waypoint(p4)
            result = uut.get_last_velocity(p5)
            expected = 2
            self.assertEqual(expected, result)

        run()

    @patch('log_book.application.stream_processor.StreamProcessor.get_last_velocity', return_value=1)
    @patch('log_book.application.stream_processor.StreamProcessor.update_distance', new_callable=MagicMock)
    def test_process_waypoint(self, _get_distance_mock, _):
        uut = StreamProcessor()

        def update_distance(new_point):
            pass

        _get_distance_mock.side_effect = update_distance

        def run():
            p0 = WayPoint(lat=1, lng=1, timestamp=datetime(year=2019, month=12, day=12, second=0))
            p1 = WayPoint(lat=1, lng=1, timestamp=datetime(year=2019, month=12, day=12, second=5))
            p2 = WayPoint(lat=1.001, lng=1.001, timestamp=datetime(year=2019, month=12, day=12, second=10))
            p3 = WayPoint(lat=1.002, lng=1.002, timestamp=datetime(year=2019, month=12, day=12, second=20))
            p4 = WayPoint(lat=1.002000001, lng=1.002000001, timestamp=datetime(year=2019, month=12, day=12, minute=1))
            p5 = WayPoint(lat=1.002000003, lng=1.002000003, timestamp=datetime(year=2019, month=12, day=12, minute=4))

            uut.process_waypoint(p0)
            uut.process_waypoint(p1)
            result = uut.process_waypoint(p2)
            expected = None
            self.assertEqual(expected, result)

            result = uut.process_waypoint(p3)
            expected = None
            self.assertEqual(expected, result)

            uut.process_waypoint(p4)
            result = uut.process_waypoint(p5)

            # locations of p0 and p1 are the same but vehicle started moving at the p1 timestamp
            self.assertEqual(p1, result.start)

            self.assertEqual(0, result.distance)

            # location of p3, p4, and p5 are very close to each other so the trip
            # should be ended at p3 and movement to p4 and p5 should not be counted.
            self.assertEqual(p3, result.end)

        run()

    @patch('log_book.application.stream_processor.haversine_distance', return_value=20)
    @patch('log_book.models.models.haversine_distance', return_value=20)
    def test_update_distance(self, _, __):
        uut = StreamProcessor()

        def run():
            p1 = WayPoint(lat=1, lng=1, timestamp=datetime(year=2019, month=12, day=12))
            p2 = WayPoint(lat=1.001, lng=1.001, timestamp=datetime(year=2019, month=12, day=12, second=10))
            p3 = WayPoint(lat=1.002, lng=1.002, timestamp=datetime(year=2019, month=12, day=12, second=20))
            p4 = WayPoint(lat=1.002, lng=1.002, timestamp=datetime(year=2019, month=12, day=12, minute=4))

            uut.process_waypoint(p1)
            uut.process_waypoint(p2)
            uut.process_waypoint(p3)
            uut.process_waypoint(p4)

            self.assertEqual(60, uut.trip.distance)

        run()

    @patch('log_book.application.stream_processor.StreamProcessor.get_last_velocity', return_value=40)
    def test_jump(self, _):
        uut = StreamProcessor()

        def run1():
            p0 = WayPoint(lat=1, lng=1, timestamp=datetime(year=2019, month=12, day=12, second=0))
            p1 = WayPoint(lat=1, lng=1, timestamp=datetime(year=2019, month=12, day=12, second=5))
            uut.process_waypoint(p0)
            uut.process_waypoint(p1)
            self.assertEqual(p0, uut.last_way_point)
            self.assertEqual(0, uut.trip.distance)

        run1()
