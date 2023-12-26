import logging

from celery import Celery

from config import REDIS_HOST

from app.database import get_db
from app.models import MD5Result, MD5Status
from app.utils import calculate_actual_md5

celery = Celery(
    "tasks",
    broker=REDIS_HOST,
    backend=REDIS_HOST,
    broker_connection_retry_on_startup=True,
    worker_hijack_root_logger=False,
)


@celery.task
def calculate_md5(file_path: str, promise_id: str):
    db = get_db()
    pending = None

    try:
        pending = MD5Result(promise_id=promise_id, status=MD5Status.PENDING)
        db.add(pending)
        db.commit()

        md5_hash = calculate_actual_md5(file_path)

        pending.md5_hash = md5_hash
        pending.status = MD5Status.SUCCESS
        db.commit()

        logging.info(f"Promise ID: {promise_id}, MD5 Hash: {md5_hash}, Status: success")
    except Exception as e:
        if pending:
            pending.status = MD5Status.FAILED
            db.commit()

        logging.error(f"Error processing promise_id {promise_id}: {str(e)}", exc_info=True)
