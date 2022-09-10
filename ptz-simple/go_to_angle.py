#!/usr/bin/env python

import pantilthat
import time
import sys

angle = int(sys.argv[1])

print(angle)
pantilthat.pan(angle)
time.sleep(1)
