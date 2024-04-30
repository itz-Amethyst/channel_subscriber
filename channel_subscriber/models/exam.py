from typing import Union , List , Dict

from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import RangeBoundary , RangeOperators
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F , Q
from django.utils import timezone

from core.models import Teacher
from core.models.core import CoreModel
from channel_subscriber.models import Lesson , Class
from django.utils.translation import gettext_lazy as _

from channel_subscriber.models.helper.constraint.time_range import TsTzRange


class Exam(CoreModel):
    title = models.CharField(
        verbose_name = _("Title") ,
        help_text = _("this is the title for a exam") ,
        db_comment = _("this is the title for a exam") ,
        max_length=100
    )

    teacher: models.ForeignKey[Teacher] = models.ForeignKey(
        Teacher ,
        verbose_name = _("Teacher") ,
        help_text = _("this is the teacher for a class") ,
        db_comment = _("this is the teacher for a class") ,
        on_delete = models.CASCADE ,

    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name=_("Lesson"),
        help_text=_("The lesson associated with this exam"),
        db_comment=_("The lesson associated with this exam")
    )
    classes = models.ManyToManyField(
        Class,
        verbose_name=_("Classes"),
        help_text=_("Select the classes for which this exam is intended"),
    )
    time_start: models.DateTimeField = models.DateTimeField(
        verbose_name = _("Time Start") ,
        help_text = _("this is the time start for a class") ,
        db_comment = _("this is the time start for a class") ,
    )

    time_end: models.DateTimeField = models.DateTimeField(
        verbose_name = _("Time End") ,
        help_text = _("this is the time ends for a class") ,
        db_comment = _("this is the time ends for a class") ,
    )

    class Meta:
        db_table: str = "exam"
        db_table_comment: str = _("This is a table for all school exams.")
        verbose_name: str = _("Exam")
        verbose_name_plural: str = _("Class Rooms")
        ordering: Union[str , list] = ["-created_at" , "title"]

        constraints: list = [

            models.CheckConstraint(
                check = models.Q(created_at__gte = models.ExpressionWrapper(models.Value("NOW()") ,output_field = models.DateTimeField())) ,
                name = "created_at_gte_now_exam" ,
                violation_error_message = _("The created at time must be greater than or equal to the current time.")
            ) ,

            ExclusionConstraint(
                name = 'exclude_overlapping_exams' ,
                expressions = (
                    (TsTzRange('time_start' , 'time_end' , RangeBoundary()) , RangeOperators.OVERLAPS) ,
                    ('teacher' , RangeOperators.EQUAL) ,
                ) ,
            ) ,
            models.CheckConstraint(
                check = (Q(time_start__gte = F('created_at')) & Q(time_start__gte = models.ExpressionWrapper(models.Value('NOW()') ,output_field = models.DateTimeField())) &
                        Q(time_end__gt = F('time_start')) & Q(
                    time_end__gt = models.ExpressionWrapper(models.Value('NOW()') ,output_field = models.DateTimeField())) &
                        Q(time_end__gt = F('created_at')) & Q(
                    time_end__gt = models.ExpressionWrapper(models.Value('NOW()') ,output_field = models.DateTimeField()))
                ) ,
                name = 'exam_time_constraints' ,
                violation_error_message = _("The exam time constraints are violated.")
            )
        ]

    def clean(self) -> None:
        """
        Clean the class time constraints.
        """
        current_time: timezone.datetime = timezone.now()

        if self.time_start < self.created_at or self.time_start < current_time:
            raise ValidationError(
                {"time_start": _("Time start must be greater than or equal to created at and not in the past.")}
            )

        if self.time_end <= self.time_start or self.time_end <= current_time:
            raise ValidationError(
                {"time_end": _("Time end must be greater than time start and not in the past.")}
            )

        if self.time_end <= self.created_at or self.time_end <= current_time:
            raise ValidationError(
                {"time_end": _("Time end must be greater than created at and not in the past.")}
            )

        super().clean()

    def save(self, *args: List, **kwargs: Dict) -> None:
        """
        Override the save method to perform validation before saving.
        """
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.lesson}"