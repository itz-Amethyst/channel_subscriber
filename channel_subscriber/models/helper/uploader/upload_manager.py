import os
from django.utils import timezone
from kernel.settings.development.settings import MEDIA_ROOT

def file_upload_path(instance, filename, path):
    current_date = timezone.now().strftime('%Y-%m-%d')
    filename = "{}-{}".format(current_date, filename)
    return os.path.join(MEDIA_ROOT, "files" , path, current_date , filename)


expected_path: str = os.path.join(MEDIA_ROOT, 'files' , timezone.now().strftime('%Y-%m-%d'))
