import time

import os

i = 0

while(i<50000):
    i += 1
    os.system(
        "python .\main.py --solve condiscr"
    )
    # time.sleep(0.001)