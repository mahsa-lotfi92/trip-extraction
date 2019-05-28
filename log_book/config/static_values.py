from datetime import timedelta

IGNORE_DISTANCE = 15 # meter
MAX_TIME_WITHOUT_MOVEMENT = timedelta(minutes=3)
MAX_ACCEPTABLE_VELOCITY = 30 # = 108 km/h