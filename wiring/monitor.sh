#!/usr/bin/env bash
stty -F /dev/ttyUSB0 57600 cs8 cread clocal && cat < /dev/ttyUSB0
