from celery import shared_task
from django.core.management import call_command
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task
def run_add_youtube_data():
    logger.info("Running the command: update_channels_live")
    call_command("update_channels_live")
