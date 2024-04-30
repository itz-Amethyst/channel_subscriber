from django.core.validators import RegexValidator

YOUTUBE_CHANNEL_REGEX = r'^https://youtube\.com/channel/.*$'

# Validator using the defined regex pattern
youtube_channel_validator = RegexValidator(
    regex=YOUTUBE_CHANNEL_REGEX,
    message="The URL must start with 'https://youtube.com/channel/'"
)