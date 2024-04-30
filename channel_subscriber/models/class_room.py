from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q, Func
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import (
    RangeBoundary,
    RangeOperators, )
from core.models import Teacher, Student, Assistant, User
from core.models.core import CoreModel
from channel_subscriber.models.class_room_students import ClassRoomStudent

from channel_subscriber.models.helper.constraint.time_range import TsTzRange
from channel_subscriber.models.helper.constraint.file_path_validator_reg import file_path_validator
from typing import Union, Dict, List
from channel_subscriber.models.helper.managers.class_room import ClassManager

class Class(CoreModel):
    """
    the Class model Represents a classroom in the system.

    Attributes:
        name (CharField): Name of the class.
        created_at (DateTimeField:auto add): Time that the class is created.
        time_start (DateTimeField): Time start for the class.
        time_end (DateTimeField): Time end for the class.

    Relations:
        user (ForeignKey): One-to-many relationship with the User(admin) model.
        teacher (ForeignKey): One-to-many relationship with the Teacher model.
        assistant (ForeignKey): One-to-many relationship with the Assistant model.
        students (ManyToManyField): Many-to-many relationship with the Student model.
    """

    user: models.ForeignKey[User] = models.ForeignKey(
        to=User,
        verbose_name=_("User"),
        help_text=_("this is the user(admin) for a class"),
        db_comment=_("this is the user(admin) for a class"),
        on_delete=models.CASCADE,
        editable=True,
        db_column=_("user_id"),

    )

    teacher: models.ForeignKey[Teacher] = models.ForeignKey(
        Teacher,
        verbose_name=_("Teacher"),
        help_text=_("this is the teacher for a class"),
        db_comment=_("this is the teacher for a class"),
        on_delete=models.CASCADE,
        editable=True,
        db_column=_("teacher_id")

    )
    assistant: models.ForeignKey[Assistant] = models.ForeignKey(
        Assistant,
        verbose_name=_("Assistant"),
        help_text=_("this is the assistant for a class"),
        db_comment=_("this is the assistant for a class"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        editable=True,
        db_column=_("assistant_id")
    )
    # Todo
    students: models.ManyToManyField = models.ManyToManyField(
        Student,
        verbose_name=_("Students"),
        help_text=_("The students of the class"),
        blank=True,
        through = ClassRoomStudent,
        through_fields = ['class_room', 'student'],
        related_name = 'classes',
        # editable=True,
        db_column=_("student_id")
    )
    name: models.CharField = models.CharField(
        verbose_name=_("Name"),
        help_text=_("The name of the class"),
        db_comment=_("The name of the class"),
        unique=True,
        editable=True,
        max_length = 255,
        db_column=_("Name"),
        error_messages={
            'required': _('Name is required. Please provide a name for the Class.'),
            'unique': _('a class with this name already exists. Please provide another name for the Class.')
        }
    )

    time_start: models.DateTimeField = models.DateTimeField(
        verbose_name=_("Time Start"),
        help_text=_("this is the time start for a class"),
        db_comment=_("this is the time start for a class"),
        editable=True,
        db_column=_("Time Start"),
    )

    time_end: models.DateTimeField = models.DateTimeField(
        verbose_name=_("Time End"),
        help_text=_("this is the time ends for a class"),
        db_comment=_("this is the time ends for a class"),
        editable=True,
        db_column=_("Time End"),
    )

    # lessons: models.ManyToManyField = models.ManyToManyField(
    #     'Lesson' ,
    #     verbose_name = _("Lessons") ,
    #     related_name = 'class_rooms_lessons',
    #     help_text = _("These are the lessons for this class") ,
    # )

    section: models.ForeignKey = models.ForeignKey(
        'Section' ,
        verbose_name = _("Section") ,
        help_text = _("The section associated with this class") ,
        db_comment = _("The section associated with this class") ,
        on_delete = models.SET_NULL ,
        null = True ,
        blank = True ,
        related_name = 'classes'
    )

    objects: models.Manager[ClassManager] = ClassManager()

    class Meta:
        db_table: str = "class_rooms"
        db_table_comment: str = _("This is a table for all school class rooms.")
        verbose_name: str = _("Class Room")
        verbose_name_plural: str = _("Class Rooms")
        ordering: Union[str, list] = ["-created_at", "name"]

        constraints: list = [

            models.CheckConstraint(
                check = models.Q(created_at__gte = models.ExpressionWrapper(models.Value("NOW()"), output_field = models.DateTimeField())) ,
                name = "created_at_gte_now_class_room" ,
                violation_error_message = _("The created at time must be greater than or equal to the current time.")
            ) ,

            ExclusionConstraint(
                name='exclude_overlapping_classes',
                expressions=(
                    (TsTzRange('time_start', 'time_end', RangeBoundary()), RangeOperators.OVERLAPS),
                    ('teacher', RangeOperators.EQUAL),
                ),
            ),
            models.CheckConstraint(
                check=(
                        Q(time_start__gte=F('created_at')) & Q(
                    time_start__gte=models.ExpressionWrapper(models.Value('NOW()'),
                                                             output_field=models.DateTimeField())) &
                        Q(time_end__gt=F('time_start')) & Q(
                    time_end__gt=models.ExpressionWrapper(models.Value('NOW()'), output_field=models.DateTimeField())) &
                        Q(time_end__gt=F('created_at')) & Q(
                    time_end__gt=models.ExpressionWrapper(models.Value('NOW()'), output_field=models.DateTimeField()))
                ),
                name='class_time_constraints',
                violation_error_message=_("The class time constraints are violated.")
            )
        ]

        indexes: list = [
            models.Index(
                name = "class_section_idx" ,
                fields = ["section"] ,
            )
        ]

    #! Not sure
    def is_exceeded(self) -> bool:
        """
        Check if the class time ended.
        """
        return timezone.now() > self.time_end


    def __str__(self) -> str:
        """
        Return string representation of class.
        """
        return self.name

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
