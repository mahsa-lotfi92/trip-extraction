import json
import sys
from datetime import datetime
from json.decoder import JSONDecodeError

from log_book.runner.processor import process_way_points


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def runner():
    if len(sys.argv) <= 1:
        print('Please provide a file name to read the waypoint data')
        sys.exit(1)

    with open(sys.argv[1]) as json_file:
        try:
            way_points = json.loads(json_file.read())
            trips = process_way_points(way_points)
            with open("trips.json", 'w') as trips_file:
                trips_file.write(json.dumps(trips, cls=Encoder))
        except JSONDecodeError:
            print('Input file should be json file.')
            sys.exit(1)
