from log_book.models.models import Trip


class TripEntity:
    def __init__(self, start=None, end=None, distance=0):
        self.start = start
        self.end = end
        self.distance = distance

    def to_trip(self):
        return Trip(start=self.start, end=self.end, distance=self.distance)

    def __repr__(self):
        return 'Start: {}, End:{}, Distance:{}'.format(self.start, self.end, self.distance)