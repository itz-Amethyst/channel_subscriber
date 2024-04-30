from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import Teacher
from core.models.core import CoreModel
from channel_subscriber.models.helper.enums.paths import PathOptions
from channel_subscriber.models.helper.managers.lesson import LessonManager
from channel_subscriber.models.helper.uploader.replace import replace_old_with_new_one
from channel_subscriber.models.helper.uploader.upload_manager import file_upload_path , expected_path
from channel_subscriber.models.section import Section
from channel_subscriber.models.class_room import Class
from django.core.exceptions import ValidationError
from django.utils import timezone
import os
from channel_subscriber.models.helper.constraint.file_path_validator_reg import file_path_validator
from channel_subscriber.validators.files.validate_file_ext import validate_file_extension
from channel_subscriber.validators.files.validate_file_path import validate_file_name_matches_folder_name
from channel_subscriber.validators.files.validate_file_size import validate_file_size
from channel_subscriber.validators.files.validate_file_type import validate_file_type

from django.utils.safestring import mark_safe
import bleach
from typing import Dict, List

class Lesson(CoreModel):
    """
        Lessen model Represents a lesson in the system.

        Attributes:
            name (CharField): Name of the lesson.
            text (TextField): Text of the lesson.
            file (FileField): File of the lesson.
            created_at (DateTimeField:auto add): Time that the lesson is created.

        Relations:
            teacher (ForeignKey): One-to-many relationship with the Teacher model.
            class_room (ForeignKey): Many-to-many relationship with the Class model.
        """

    def _file_upload_path( self , filename ):
        return file_upload_path(self , filename , PathOptions.LESSONS)

    teacher: models.ForeignKey[Teacher] = models.ForeignKey(
        to=Teacher,
        verbose_name=_("Teacher"),
        help_text=_("this is the teacher that set this lesson"),
        db_comment=_("this is the teacher that set this lesson"),
        on_delete=models.CASCADE,
        editable=True,
        db_column=_("teacher_id")
    )
    class_room: models.ManyToManyField = models.ManyToManyField(
        to=Class,
        verbose_name=_("Class Room"),
        help_text=_("this is the lessons for a class"),
        # db_comment=_("this is the lessons for a class"),
        # on_delete=models.CASCADE,
        related_name="lessons",
        editable=True,
        db_column=_("class_id"),

    )

    name: models.CharField = models.CharField(
        verbose_name=_("Name"),
        help_text=_("this is the name for a lesson"),
        db_comment=_("this is the name for a lesson"),
        unique=True,
        editable=True,
        max_length = 255,
        db_column=_("Name"),
        error_messages={
            "required": _("Name is required. Please provide a name for the Lesson."),
            "unique": _("Lesson with this name already exists. Please provide another name for the Lesson.")
        }
    )

    text: models.TextField = models.TextField(
        verbose_name=_("Text"),
        help_text=_("this is the text for a lesson"),
        db_comment=_("this is the text for a lesson"),
        blank=True,
        null=True,
        editable=True,
        db_column=_("Text")
    )

    file: models.FileField = models.FileField(
        verbose_name=_("File"),
        help_text=_("this is file for a lesson"),
        db_comment=_("this is file for a lesson"),
        upload_to=_file_upload_path,
        editable=True,
        db_column=_("File"),
        validators=[
            validate_file_extension,
            validate_file_size,
            validate_file_type,
            validate_file_name_matches_folder_name
        ]
    )



    section: models.ForeignKey[Section] = models.ForeignKey(
        Section ,
        verbose_name = _("Section") ,
        help_text = _("The section associated with this lesson") ,
        db_comment = _("The section associated with this lesson") ,
        on_delete = models.SET_NULL ,
        null = True ,
        blank = True,
        related_name = 'lessons'
    )

    is_primary: models.BooleanField = models.BooleanField(
        verbose_name = _("Is Primary") ,
        help_text = _("Whether this lesson is a primary lesson") ,
        db_comment = _("Whether this lesson is a primary lesson") ,
        default = False
    )

    objects: models.Manager[LessonManager] = LessonManager()


    class Meta:
        db_table: str = "lessons"
        db_table_comment: str = _("This is a table for all class room lessons.")
        verbose_name: str = _("Lesson")
        verbose_name_plural: str = _("Lessons")
        constraints: list = [
            models.CheckConstraint(
                check=models.Q(created_at__gte=models.ExpressionWrapper(models.Value('NOW()'),
                                                                        output_field=models.DateTimeField())),
                name="created_at_gte_now_lesson",
                violation_error_message=_("The created at time must be greater than or equal to the current time.")
            ),
            models.CheckConstraint(
                check=models.Q(file__regex=file_path_validator.regex.pattern),
                name='valid_file_path_format_lesson',
                violation_error_message = _(file_path_validator.message)
            )
        ]

        # If the relation is Foreign uncomment this
        # indexes: list = [
        #     models.Index(
        #         name = "lesson_class_room_idx" ,
        #         fields = ["class_room"] ,
        #     )
        # ]

    def __str__( self ):
        return f"{self.name} - ({', '.join(str(cls_room) for cls_room in self.class_room)}) - {self.section}"


    def clean(self) -> None:
        """
        Clean the lesson constraints.
        """
        current_date_prefix = timezone.now().strftime('%Y-%m-%d')

        # Check if file path matches expected format
        if self.file.path != expected_path:
            raise ValidationError(
                {'file': _(
                    'Invalid upload path format. The correct format is %(expected)s.' % {'expected': expected_path})} ,
                params = {'expected': expected_path} ,
            )

        # Ensure file name starts with current date in the format YYYYMMDD
        file_name = os.path.basename(self.file.name)
        if not file_name.startswith(current_date_prefix):
            raise ValidationError(
                {'file': _("File name must start with the current date in the format YYYYMMDD.")}
            )

        super().clean()

    # def sanitized_text(self) -> str:
    #     """
    #     Return sanitized text to prevent XSS attacks.
    #
    #     This method allows only specific safe HTML tags and attributes.
    #
    #     Returns:
    #         str: Sanitized text with only allowed HTML tags and attributes.
    #     """
    #     allowed_tags: List[str] = [
    #         'a', 'abbr', 'acronym', 'address', 'b', 'bdo', 'big', 'blockquote', 'br', 'caption', 'cite', 'code',
    #         'col', 'colgroup', 'dd', 'del', 'dfn', 'div', 'dl', 'dt', 'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    #         'hr', 'i', 'img', 'ins', 'kbd', 'li', 'ol', 'p', 'pre', 'q', 'samp', 'small', 'span', 'strike',
    #         'strong', 'sub', 'sup', 'table', 'tbody', 'td', 'tfoot', 'th', 'thead', 'tr', 'tt', 'u', 'ul', 'var'
    #     ]
    #
    #     allowed_attributes: Dict[str, List[str]] = {
    #         '*': ['title', 'style'],
    #         'a': ['href', 'title'],
    #         'img': ['src', 'alt'],
    #     }
    #
    #     return mark_safe(bleach.clean(self.text, tags=allowed_tags, attributes=allowed_attributes))

    def save(self, *args: List, **kwargs: Dict) -> None:
        """
        Override the save method to perform validation before saving.
        """
        self.clean()

        replace_old_with_new_one(instance = self , model = Lesson)
        super().save(*args, **kwargs)
