from typing import Union

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from core.models import Student


class ClassRoomStudent(models.Model):
    class_room: models.ForeignKey = models.ForeignKey('Class', on_delete=models.CASCADE)
    student: models.ForeignKey[Student] = models.ForeignKey(Student, on_delete=models.CASCADE)
    date_joined: models.DateTimeField = models.DateTimeField(
        verbose_name = _("Date Joined") ,
        help_text = _("the time that user joined class") ,
        db_comment = _("the time that user joined class") ,
        auto_now_add = True
    )

    constraints: list = [

        models.CheckConstraint(
            check = models.Q(date_joined__gte = models.ExpressionWrapper(models.Value("NOW()") ,output_field = models.DateTimeField())) ,
            name = "date_joined_gte_now_class_rooms_students" ,
            violation_error_message = _("The date_joined time must be greater than or equal to the current time.")
        ) ,
    ]

    class Meta:
        db_table: str = "class_rooms_students"
        db_table_comment: str = _("This is a table for all classroom's associated with students.")
        verbose_name: str = _("class_rooms_students")
        verbose_name_plural: str = _("Class_Rooms_Students")
        ordering: Union[str , list] = ["-date_joined"]
        unique_together = ['class_room', 'student']


    def clean(self) -> None:
        """
        Clean the ClassRoomStudent time constraints.
        """

        if self.date_joined < timezone.now():
            raise ValidationError(
                _('The date joined time must be greater than or equal to the current time.'),
                code='invalid'
            )

    def save(self, *args, **kwargs) -> None:
        """
        Override the save method to perform validation before saving.
        """
        self.clean()
        super().save(*args, **kwargs)
