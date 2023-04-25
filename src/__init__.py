"""INIT FILE"""
from celery import Celery

celery1 = Celery('task', config_source='src.celeryconfig')
