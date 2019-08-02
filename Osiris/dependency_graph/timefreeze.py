from freezegun import freeze_time
import datetime
import time
freezer = freeze_time("2012-01-14 12:00:01")
freezer.start()
assert datetime.datetime.now() == datetime.datetime(2012, 1, 14, 12, 0, 1)
print(time.time())
print(datetime.datetime.now())
print(time.time())
freezer.stop()
