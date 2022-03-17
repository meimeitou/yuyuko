import multiprocessing
import os

import gevent.monkey
from dotenv import load_dotenv
from smart_getenv import getenv

gevent.monkey.patch_all()
cores = multiprocessing.cpu_count()

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
load_dotenv(os.path.join(basedir, '/etc/yuyuko/.env'))

bind = '0.0.0.0:5588'
graceful_timeout = 360
timeout = 3600
preload_app = True
keep_alive = 100
max_requests = 120
workers = getenv('WORKER_NUM', default=cores * 2)
log_level = 'info'
debug = True
accesslog = '-'
access_log_format = ('%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" '
                     '"%(a)s" %(D)s %({X-Docker-Size}o)s')
