from celery import shared_task
from .services import create_global_snapshot

@shared_task
def create_daily_snapshot_task():
    snapshot = create_global_snapshot()
    return snapshot.id
