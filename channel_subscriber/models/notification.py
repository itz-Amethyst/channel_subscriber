from django.db import models

from channel_subscriber.models.section import Section
from django.utils.translation import gettext_lazy as _


class Notification(models.Model):
    title = models.CharField(
        max_length = 170,
        verbose_name = _("Title"),
        help_text = _("The title of notification"),
        db_comment = _("The title of notification")
    )
    content = models.TextField(
        verbose_name = _("Content"),
        help_text = _("The content of notification") ,
        db_comment = _("The content of notification")
    )

    target_section = models.ForeignKey(
        Section ,
        verbose_name = _("Target Section") ,
        help_text = _("Select the section for which this notice is intended") ,
        db_comment = _("Section targeted by this notice") ,
        on_delete = models.SET_NULL ,
        null = True ,
        blank = True
    )

    target_classes = models.ManyToManyField(
        'Class' ,
        verbose_name = _("Target Classes") ,
        help_text = _("Select the classes for which this notice is intended") ,
        db_column = _("Select the classes for which this notice is intended") ,
    )

    #! To Target specific section and send notif to all of their associated classes
    def save(self , *args, **kwargs):
        if self.target_section:
            self.target_classes.set(self.target_section.classes.all())
        super().save(*args, **kwargs)

    def __str__( self ):
        return self.title
