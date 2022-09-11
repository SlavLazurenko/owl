#!/usr/bin/env python

import pantilthat
import time
import sys

angle = int(sys.argv[1])
elevation = int(sys.argv[2])

print(angle)
pantilthat.pan(angle)
pantilthat.tilt(elevation)
time.sleep(1)
