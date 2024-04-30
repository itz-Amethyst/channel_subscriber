from typing import Union , Dict

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import os

from core.models.core import CoreModel
from channel_subscriber.models.helper.enums.paths import PathOptions
from channel_subscriber.models.helper.managers.question import QuestionManager
from channel_subscriber.models.helper.uploader.replace import replace_old_with_new_one
from channel_subscriber.models.helper.uploader.upload_manager import file_upload_path , expected_path
from channel_subscriber.models.lesson import Lesson
from core.models import Teacher , Assistant
from channel_subscriber.models.helper.constraint.file_path_validator_reg import file_path_validator
from channel_subscriber.validators.files.validate_file_ext import validate_file_extension
from channel_subscriber.validators.files.validate_file_path import validate_file_name_matches_folder_name
from channel_subscriber.validators.files.validate_file_size import validate_file_size
from channel_subscriber.validators.files.validate_file_type import validate_file_type
from django.utils.safestring import mark_safe
import bleach
from typing import Dict, List

class Question(CoreModel):
    """
        Represents a question in a lesson.

        Attributes:
            name (CharField): The name of the question.
            text (TextField): The text of the question.
            file (FileField): The file for the question.
            created_at (DateTimeField:auto add): The time that the question is created.
            expire_time (DateTimeField): The time that the question is expired.

        Relations:
            teacher (ForeignKey): The teacher who set this question for a lesson.
            assistant (ForeignKey): The assistant who set this question for a lesson.
            lesson (ForeignKey): The lesson that this question belongs to.
        """

    def _file_upload_path( self , filename ):
        return file_upload_path(self , filename , PathOptions.QUESTIONS)

    teacher: models.ForeignKey[Teacher] = models.ForeignKey(
        to=Teacher,
        verbose_name=_("Teacher"),
        help_text=_("this is the teacher that set this question for a lesson"),
        db_comment=_("this is the teacher that set this question for a lesson"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        editable=True,
        db_column=_("teacher_id")
    )
    assistant: models.ForeignKey[Assistant] = models.ForeignKey(
        to=Assistant,
        verbose_name=_("Assistant"),
        help_text=_("this is the assistant that set this question for a lesson"),
        db_comment=_("this is the assistant that set this question for a lesson"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        editable=True,
        db_column=_("assistant_id")
    )
    lesson: models.ForeignKey[Lesson] = models.ForeignKey(
        to=Lesson,
        verbose_name=_("Lesson"),
        help_text=_("this mean the lesson has many question"),
        db_comment=_("this mean the lesson has many question"),
        on_delete=models.CASCADE,
        related_name="lesson_questions",
        editable=True,
        db_column=_("lesson_id")
    )
    name: models.CharField = models.CharField(
        verbose_name=_("Name"),
        help_text=_("this is the name for a question"),
        db_comment=_("this is the name for a question"),
        unique=True,
        editable=True,
        max_length = 255,
        db_column=_("Name"),
        error_messages={
            'required': _('Name is required. Please provide a name for the question.'),
            'unique': _('this question already exists.')
        }
    )

    text: models.TextField = models.TextField(
        verbose_name=_("Text"),
        help_text=_("this is the text for a question"),
        db_comment=_("this is the text for a question"),
        blank=True,
        null=True,
        editable=True,
        db_column=_("Text")
    )

    file: models.FileField = models.FileField(
        verbose_name=_("File"),
        help_text=_("this is file for a question"),
        db_comment=_("this is file for a question"),
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


    expire_time: models.DateTimeField = models.DateTimeField(
        verbose_name=_("Expire Time"),
        help_text=_("the time that the question is expire"),
        db_comment=_("the time that the question is expire"),
        editable=True,
        db_column=_("Expire time")
    )

    objects: models.Manager[QuestionManager] = QuestionManager()

    class Meta:
        db_table: str = "questions"
        db_table_comment: str = _("This is a table for all questions of each lesson.")
        verbose_name: str = _("Question")
        verbose_name_plural: str = _("Questions")
        ordering: Union[str, list] = ["-created_at"]

        constraints: list = [
            models.CheckConstraint(
                check=models.Q(expire_time__gt=models.F("created_at")),
                name="expire_time_greater_than_created_at",
                violation_error_message=_("The expiration time is not valid.")
            ),
            models.CheckConstraint(
                check=models.Q(teacher__isnull=False) | models.Q(assistant__isnull=False),
                name="teacher_or_assistant_is_not_null",
                violation_error_message=_("The question must be set by a teacher or assistant.")
            ),
            models.CheckConstraint(
                check=models.Q(created_at__gte=models.ExpressionWrapper(models.Value('NOW()'),
                                                                        output_field=models.DateTimeField())) & models.Q(
                    expire_time__gt=models.ExpressionWrapper(models.Value('NOW()'),
                                                             output_field=models.DateTimeField())),
                name="time_constraints",
                violation_error_message=_(
                    "The created at time must be greater than or equal to now, and the expiration time must be greater than now.")
            ),
            models.CheckConstraint(
                check=models.Q(file__regex=file_path_validator.regex.pattern),
                name='valid_file_path_format_question',
                violation_error_message = _(file_path_validator.message)
            )
        ]

        indexes: list = [
            models.Index(
                name = "question_lesson_idx" ,
                fields = ["lesson"] ,
            )
        ]

    def is_expired(self) -> bool:
        """
        Check if the question is expired.
        """
        return timezone.now() > self.expire_time

    def clean(self) -> None:
        """
        Clean the question's time constraints.
        """
        current_date_prefix = timezone.now().strftime('%Y-%m-%d')

        # Check if file path matches expected format
        if self.file.path != expected_path:
            raise ValidationError(
                {'file': _(
                    'Invalid upload path format. The correct format is %(expected)s.' % {'expected': expected_path})},
                params={'expected': expected_path},
            )

        # Ensure file name starts with current date in the format YYYYMMDD
        file_name = os.path.basename(self.file.name)
        if not file_name.startswith(current_date_prefix):
            raise ValidationError(
                {'file': _("File name must start with the current date in the format YYYYMMDD.")}
            )
        if self.expire_time <= self.created_at:
            raise ValidationError(
                {"expire_time": _("The expiration time must be greater than the create time.")}
            )

        if self.teacher is None and self.assistant is None:
            raise ValidationError(
                {"teacher": _("Either the teacher or assistant field must be set.")}
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

    def save( self , *args: list , **kwargs: Dict ) -> None:
        """
        Override the save method to perform validation before saving.
        """
        self.clean()
        replace_old_with_new_one(instance = self , model = Question)
        super().save(*args , **kwargs)
