from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models.core import CoreModel
from django.core.exceptions import ValidationError
from channel_subscriber.models.helper.constraint.url_path_validator_reg import youtube_channel_validator , YOUTUBE_CHANNEL_REGEX

from typing import Dict, List
from channel_subscriber.models.helper.managers.channel import  ChannelManager


class Channel(CoreModel):
    """
    The `Channel` model represents a multimedia content channel owned by a user.

    Attributes:
        owner (ForeignKey): The user who owns this channel.
        title (CharField): The title of the channel.
        content (CharField): Optional description of the channel.
        url (URLField): The YouTube channel URL, which must start with 'https://youtube.com/channel/'.

    Relations:
        None specified in this example.
    """

    owner: models.ForeignKey[settings.AUTH_USER_MODEL] = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name=_("owner"),
        help_text=_("this is the owner that owns this channel"),
        db_comment=_("this is the owner that owns this channel"),
        on_delete=models.CASCADE,
        # editable=True,
        db_column=_("owner_id"),
    )

    title: models.CharField = models.CharField(
        verbose_name=_("Title"),
        help_text=_("this is the title for the channel"),
        db_comment=_("this is the title for the channel"),
        editable=True,
        db_column=_("Title"),
        error_messages={
            'required': _('Title is required. Please provide a Title for the channel.')
        },
        max_length=255
    )

    content: models.CharField = models.CharField(
        verbose_name=_("Content"),
        help_text=_("this is the content for the channel"),
        db_comment=_("this is the content for the channel"),
        blank=True,
        null=True,
        editable=True,
        db_column=_("Content")
    )

    url: models.URLField = models.URLField(
        max_length = 200 ,
        validators = [youtube_channel_validator] ,  # Applying regex-based validator
        help_text = "Enter a YouTube channel URL starting with 'https://youtube.com/channel/'" ,
    )

    objects: models.Manager[ChannelManager] = ChannelManager()

    class Meta:
        db_table = "channels"
        verbose_name = _("Channel")
        verbose_name_plural = _("Channels")
        ordering = ["title"]  # Ordered by title alphabetically

        constraints = [
            # Example constraint to ensure that the URL is a YouTube channel
            models.CheckConstraint(
                check = models.Q(url__regex = YOUTUBE_CHANNEL_REGEX) ,
                name = "valid_youtube_channel_url" ,
                violation_error_message = _("The URL must start with 'https://youtube.com/channel/'") ,
            ) ,
        ]

    def clean(self) -> None:
        """
        Validate the Channel before saving.
        """
        # Check if the URL starts with the required YouTube channel prefix
        if not self.url.startswith("https://youtube.com/channel/"):
            raise ValidationError(
                {'url': _("The URL must start with 'https://youtube.com/channel/'.")}
            )

        # Check if the title is empty
        if not self.title:
            raise ValidationError(
                {'title': _("The title cannot be empty.")}
            )

        # Check if there's another channel with the same title and owner,
        if not self._state.adding:  # This is an update to an existing instance
            existing_query = Channel.objects.filter(title = self.title , owner = self.owner).exclude(id = self.id)

            if existing_query.exists():
                raise ValidationError(
                    {'title': _("A channel with this title already exists for this owner.")}
                )

        # Optional: Check if content is too long (e.g., limit to 1000 characters)
        max_content_length = 1000
        if self.content and len(self.content) > max_content_length:
            raise ValidationError(
                {'content': _(f"The content cannot exceed {max_content_length} characters.")}
            )

        super().clean()




    def save(self, *args: List, **kwargs: Dict) -> None:
        """
        Override the save method to perform validation before saving.
        """
        self.clean()

        super().save(*args, **kwargs)