from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models.student import Student
from channel_subscriber.models import Lesson
from channel_subscriber.models.section import Section


class Grade(models.Model):
    lesson = models.OneToOneField(
        Lesson ,
        verbose_name = _("Lesson") ,
        help_text = _("the lesson for this Grade") ,
        db_comment = _("the lesson for this Grad") ,
        on_delete = models.CASCADE
    )
    student = models.OneToOneField(
        Student ,
        verbose_name = _("Student") ,
        help_text = _("grade associated for student") ,
        db_comment = _("grade associated for student") ,
        on_delete = models.CASCADE
    )

    sets_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name = _("Sets By") ,
        help_text = _("The user who set this grade") ,
        db_comment = _("The user who set this grade") ,
        on_delete = models.SET_NULL ,
        null = True , blank = True
    )

    section = models.ForeignKey(
        Section ,
        verbose_name = _("Section") ,
        help_text = _("The section associated with this grade") ,
        db_comment = _("The section associated with this grade") ,
        on_delete = models.CASCADE
    )

    def __str__( self ):
        return f"{self.student}'s grade for {self.lesson} in {self.section}"