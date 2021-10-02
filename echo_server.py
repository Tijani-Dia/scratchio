# Echo server program
import socket
import bdb
from scratchio.scheduler import Scheduler

HOST = 'localhost'
PORT = 50007              # Arbitrary non-privileged port

scheduler = Scheduler()
try:
    scheduler.start_serving(HOST, PORT)
except (KeyboardInterrupt, bdb.BdbQuit):
    scheduler.close()
