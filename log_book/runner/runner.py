import json
import sys
from datetime import datetime

from log_book.runner.processor import process_way_points


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def runner():
    if len(sys.argv) <= 1:
        print('Please provide a file name to read the waypoint data')
        return

    if sys.argv[1].split('.')[-1] != 'json':
        print('Input file should be json')
        return

    with open(sys.argv[1]) as json_file:
        waypoints = json.load(json_file)
        trips = process_way_points(waypoints)
        f = open("trips.json", 'w')
        f.write(json.dumps(trips, cls=Encoder))
        f.close()
