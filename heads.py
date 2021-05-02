import time
import random
import signal
import os
import sys
import numpy as np
import termios
import tty
from colorama import Fore, Back, Style
from math import *

HEIGHT = 50
WIDTH = 180
TOP_OFFSET = 6
LEFT_OFFSET = 20
INF = 1000000000
PR = 0.000001
POWERUP_VELOCITY = 2
POWERUP_TIMELIMIT = 12
POWERUP_GRAVITY = 1
LEVEL_TIME_LIMIT = 30
BOMB_DROP_VELOCITY = 1