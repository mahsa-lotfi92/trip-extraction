import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock

from log_book.application.stream_processor import StreamProcessor
from log_book.models.models import WayPoint


class StreamProcessorTest(unittest.TestCase):
    @patch('log_book.application.stream_processor.StreamProcessor.process_waypoint', new_callable=MagicMock)
    def test_get_last_velocity(self, process_waypint_mock):
        uut = StreamProcessor()
        def process_waypoint(waypoint):
            uut.way_points.append(waypoint)
            return

        process_waypint_mock.side_effect = process_waypoint

        def run1():
            uut.process_waypoint(WayPoint(lat=1, lng=1, timestamp=datetime(year=2019, month=12, day=12)))
            result = uut.get_last_velocity(WayPoint(lat=1, lng=1, timestamp=datetime(year=2019, month=12, day=12)))
            expected = 0
            self.assertEqual(expected, result)

        def run2():
            uut.process_waypoint(WayPoint(lat=1, lng=1, timestamp=datetime(year=2019, month=12, day=12, second=20)))
            result = uut.get_last_velocity(WayPoint(lat=1, lng=1, timestamp=datetime(year=2019, month=12, day=12, second=40)))
            expected = 0
            self.assertEqual(expected, result)

        def run3():
            uut.process_waypoint(WayPoint(lat=1, lng=1, timestamp=datetime(year=2019, month=12, day=12, second=20)))
            result = uut.get_last_velocity(WayPoint(lat=2, lng=2, timestamp=datetime(year=2019, month=12, day=12, second=40)))
            expected = 7861
            self.assertEqual(expected, int(result))

        run1()
        run2()
        run3()

    @patch('log_book.application.stream_processor.StreamProcessor.get_last_velocity', return_value=1)
    @patch('log_book.application.stream_processor.StreamProcessor.update_distance', new_callable=MagicMock)
    def test_process_waypoint(self, _get_distance_mock, _):
        uut = StreamProcessor()

        def update_distance():
            pass

        _get_distance_mock.side_effect = update_distance

        def run1():
            p1 = WayPoint(lat=1, lng=1, timestamp=datetime(year=2019, month=12, day=12))
            p2 = WayPoint(lat=1.001, lng=1.001, timestamp=datetime(year=2019, month=12, day=12, second=10))
            p3 = WayPoint(lat=1.002, lng=1.002, timestamp=datetime(year=2019, month=12, day=12, second=20))
            p4 = WayPoint(lat=1.002, lng=1.002, timestamp=datetime(year=2019, month=12, day=12, minute=4))

            uut.process_waypoint(p1)
            result = uut.process_waypoint(p2)
            expected = None
            self.assertEqual(expected, result)

            result = uut.process_waypoint(p3)
            expected = None
            self.assertEqual(expected, result)

            result = uut.process_waypoint(p4)

            self.assertEqual(p1, result.start)
            self.assertEqual(0, result.distance)
            self.assertEqual(p3, result.end)

        run1()

    @patch('log_book.application.stream_processor.haversine_distance', return_value=10)
    def test_update_distance(self, _):
        uut = StreamProcessor()

        def run1():
            p1 = WayPoint(lat=1, lng=1, timestamp=datetime(year=2019, month=12, day=12))
            p2 = WayPoint(lat=1.001, lng=1.001, timestamp=datetime(year=2019, month=12, day=12, second=10))
            p3 = WayPoint(lat=1.002, lng=1.002, timestamp=datetime(year=2019, month=12, day=12, second=20))
            p4 = WayPoint(lat=1.002, lng=1.002, timestamp=datetime(year=2019, month=12, day=12, minute=4))

            uut.process_waypoint(p1)
            uut.process_waypoint(p2)
            uut.process_waypoint(p3)
            result = uut.process_waypoint(p4)

            self.assertEqual(20, result.distance)

        run1()

