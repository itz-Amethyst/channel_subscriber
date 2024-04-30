
from core.models.user import User
from django.db import models
from django.utils.translation import gettext_lazy as _



class Profile(models.Model):

    user: models.OneToOneField[User] = models.OneToOneField(
        User,
        on_delete = models.CASCADE
    )

    channel_count: models.PositiveIntegerField = models.PositiveIntegerField(
        default = 0 ,
    )
    subscriber_count: models.PositiveIntegerField = models.PositiveIntegerField(
        default = 0 ,
    )
    subscription_count: models.PositiveIntegerField = models.PositiveIntegerField(
        default = 0 ,
    )
    bio: models.CharField = models.CharField(
        max_length = 1000 ,
        null = True ,
        blank = True
    )

    class Meta:
        db_table: str = "profile"
        db_table_comment: str = "This table contains profiles for users in the system."
        verbose_name: str = _("Profile")
        verbose_name_plural: str = _("Profiles")


    def __str__( self ):
        return f"{self.user} >> {self.bio}"