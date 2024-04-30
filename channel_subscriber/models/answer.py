from django.core.files.storage import default_storage
from django.db import models
from django.utils.translation import gettext_lazy as _

from channel_subscriber.models.helper.uploader.replace import replace_old_with_new_one
from core.models.core import CoreModel
from channel_subscriber.models.helper.uploader.upload_manager import file_upload_path , expected_path
from channel_subscriber.models.question import Question
from core.models import Student
from django.utils import timezone
from channel_subscriber.models.helper.enums.answer_status import AnswerStatus
from channel_subscriber.models.helper.enums.paths import PathOptions
from django.core.exceptions import ValidationError
import os
from channel_subscriber.models.helper.constraint.file_path_validator_reg import file_path_validator
from typing import Union, Dict

from channel_subscriber.validators.files.validate_file_path import validate_file_name_matches_folder_name
from channel_subscriber.validators.files.validate_file_ext import validate_file_extension
from channel_subscriber.validators.files.validate_file_size import validate_file_size
from channel_subscriber.validators.files.validate_file_type import validate_file_type

from django.utils.safestring import mark_safe
import bleach
from typing import Dict, List
from channel_subscriber.models.helper.managers.answer import AnswerManager

class Answer(CoreModel):
    """
    Answer model representing the answer for a question.

    Attributes:
        name (CharField): Name of the answer.
        text (TextField): Text of the answer.
        file (FileField): File of the answer.
        status (CharField:choices): Status of the answer.

    Relations:
        student (OneToOneField): One-to-one relationship with the Student model.
        question (ForeignKey): Foreign key relationship with the Question model.
    """

    # Handle upload path
    def _file_upload_path( self , filename ):
        return file_upload_path(self , filename , PathOptions.ANSWERS)

    student: models.ForeignKey[Student] = models.ForeignKey(
        to=Student,
        verbose_name=_("Student"),
        help_text=_("this is the student that set this answer for a question"),
        db_comment=_("this is the student that set this answer for a question"),
        on_delete=models.CASCADE,
        editable=True,
        db_column=_("student_id"),
    )
    question: models.ForeignKey[Question] = models.ForeignKey(
        to=Question,
        verbose_name=_("Question"),
        help_text=_("this mean the question has many answers"),
        db_comment=_("this mean the question has many answers"),
        on_delete=models.CASCADE,
        related_name="answers",
        editable=True,
        db_column=_("question_id"),
    )
    name: models.CharField = models.CharField(
        verbose_name=_("Name"),
        help_text=_("this is the name for an answer"),
        db_comment=_("this is the name for an answer"),
        editable=True,
        db_column=_("Name"),
        error_messages={
            'required': _('Name is required. Please provide a name for the answer.')
        },
        max_length=255
    )

    text: models.TextField = models.TextField(
        verbose_name=_("Text"),
        help_text=_("this is the text for the answer"),
        db_comment=_("this is the text for the answer"),
        blank=True,
        null=True,
        editable=True,
        db_column=_("Text")
    )

    file: models.FileField = models.FileField(
        verbose_name=_("File"),
        help_text=_("this is file for the answer"),
        db_comment=_("this is file for the answer"),
        upload_to=_file_upload_path,
        blank=True,
        null=True,
        editable=True,
        db_column=_("File"),
        validators=[
            validate_file_extension,
            validate_file_size,
            validate_file_type,
            validate_file_name_matches_folder_name
        ]
    )

    status: models.CharField = models.CharField(
        verbose_name=_("Status"),
        help_text=_("this is the status for the answer"),
        db_comment=_("this is the status for the answer"),
        choices=AnswerStatus.choices,
        editable=True,
        max_length = 255,
        db_column=_("Status")
    )


    objects: models.Manager[AnswerManager] = AnswerManager()

    class Meta:
        db_table: str = "answers"
        db_table_comment: str = _("This is a table for all answers of each question.")
        verbose_name: str = _("Answer")
        verbose_name_plural: str = _("Answers")
        ordering: Union[str, list] = ["-created_at"]

        constraints: list = [
            models.CheckConstraint(
                check=models.Q(text__isnull=False) | models.Q(file__isnull=False),
                name="text_or_file_is_not_null",
                violation_error_message=_("The answer must have text or file.")
            ),
            # Could be moved in CoreModel but the name is main concern
            models.CheckConstraint(
                check=models.Q(created_at__gte=models.ExpressionWrapper(models.Value("NOW()"),
                                                                        output_field=models.DateTimeField())),
                name="created_at_gte_now_answer",
                violation_error_message=_("The created at time must be greater than or equal to the current time.")
            ),
            models.CheckConstraint(
                check=models.Q(status__in=AnswerStatus.values),
                name="valid_status",
                violation_error_message=_("The status of the answer must be: %(choices)s.")
            ),
            models.CheckConstraint(
                check=models.Q(file__regex=file_path_validator.regex.pattern),
                name='valid_file_path_format_answer',
                violation_error_message=_(file_path_validator.message)
            )

        ]

        indexes: list = [
            models.Index(
                name="answer_question_idx",
                fields=["question"],
            )
        ]

    def clean(self) -> None:
        """
        Validate the answer before saving.
        """
        available_choices = ', '.join([str(choice[1]) for choice in AnswerStatus.choices])
        current_date_prefix = timezone.now().strftime('%Y-%m-%d')

        # Check if file path matches expected format
        if self.file.path != expected_path:
            raise ValidationError(
                {'file': _('Invalid upload path format. The correct format is %(expected)s.' % {'expected': expected_path})},
                params={'expected': expected_path},
            )

        # Ensure file name starts with current date in the format YYYYMMDD
        file_name = os.path.basename(self.file.name)
        if not file_name.startswith(current_date_prefix):
            raise ValidationError(
                {'file': _("File name must start with the current date in the format YYYYMMDD.")}
            )

        if not self.text and not self.file:
            raise ValidationError(
                _('The answer must have text or file.'),
                code='invalid'
            )


        if self.status not in dict(AnswerStatus.choices):
            raise ValidationError(
                _(f'The status of the answer must be: {available_choices} .'),
                code='invalid'
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

        replace_old_with_new_one(instance =self ,model = Answer)

        super().save(*args, **kwargs)