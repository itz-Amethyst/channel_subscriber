import re

from django.core.validators import RegexValidator
from kernel.settings.development.settings import MEDIA_ROOT

escaped_media_root = re.escape(MEDIA_ROOT)

file_path_validator = RegexValidator(
    regex=f'^{escaped_media_root}/files/[a-zA-Z0-9_-]+/\d{{4}}/\d{{1,2}}/\d{{1,2}}/[^/]+\.[a-zA-Z0-9]+$',
    message='Invalid file path format. File should be uploaded to "files/path/YYYY/MM/DD/".',
)

