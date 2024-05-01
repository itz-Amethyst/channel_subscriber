from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import uuid


class CoreModel(models.Model):
    """
        CoreModel represents a base model providing common fields and validation logic for other models.

        Attributes:
            # uuid (models.UUIDField): Unique identifier for the instance.
            created_at (models.DateTimeField): The time the instance was created.
            modified_at (models.DateTimeField): The time the instance was last modified.
    """

    # Could be considered as id
    # uuid: models.UUIDField = models.UUIDField(
    #     default = uuid.uuid4 ,
    #     editable = False ,
    #     verbose_name = _("UUID") ,
    #     help_text = _("Unique identifier for the class.") ,
    #     db_comment = _("Unique identifier for the class.") ,
    #     db_column = _("UUID") ,
    # )

    created_at: models.DateTimeField = models.DateTimeField(
        verbose_name = _("Created At") ,
        help_text = _("The time that created") ,
        db_comment = _("The time that created") ,
        auto_now_add = True ,
        editable = False ,
        db_column = _("Created at")
    )

    modified_at: models.DateTimeField = models.DateTimeField(
        verbose_name = _("Modified At") ,
        help_text = _("The time that was last modified") ,
        db_comment = _("The time that was last modified") ,
        auto_now = True ,
        editable = False ,
        db_column = _("Modified At")
    )

    class Meta:
        abstract = True
