from freezegun import freeze_time
import datetime
import time
freezer = freeze_time("2020-01-14 12:00:01")
freezer.start()
assert datetime.datetime.now() == datetime.datetime(2020, 1, 14, 12, 0, 1)
print(time.time())
print(datetime.datetime.now())
print(time.time())

import datetime
import pandas as pd
import freezegun

print(pd.Timestamp.now())
print(datetime.datetime.now())

freezer.stop()
