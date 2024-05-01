from django.core.management.base import BaseCommand

from channel_subscriber.management.commands.helper.pageToken import read_page_token , write_page_token
from channel_subscriber.management.commands.helper.youtube import send_youtube_request , extract_channel_data
from channel_subscriber.models import Channel
from django.db import transaction
# In order to have access in .env
from kernel.settings.config.setup import *
from channel_subscriber.management.commands.helper.create_user import create_author_generate_user

class Command(BaseCommand):
    help = 'Adds real time data to channel table through youtube api'

    @transaction.atomic
    def handle(self, *args, **options):
        api_key = env('YOUTUBE_API_KEY')  # Your YouTube API key
        username = env("COMMAND_GENERATE_OWNER_NAME")

        # Read the stored page token from the file
        page_token = read_page_token()

        # Send the initial request with the stored page token
        youtube_response = send_youtube_request(api_key , page_token = page_token)

        # Extract channel information and the new page token
        channel_info_list , next_page_token = extract_channel_data(youtube_response)

        # Creates author
        user = create_author_generate_user(username = username)

        # Create new Channel objects for this user
        new_channels = []

        for channel_info in channel_info_list:
            new_channel = Channel(
                owner = user ,
                title = channel_info['title'] ,
                url = f"https://youtube.com/channel/{channel_info['channelId']}",
                content = channel_info['content']
            )
            new_channels.append(new_channel)

        # Bulk create the channels for efficiency
        Channel.objects.bulk_create(new_channels)

        print(f"Created {len(new_channels)} channels for user '{username}'.")

        # Update the stored page token if there's a new token
        if next_page_token:
            write_page_token(next_page_token)