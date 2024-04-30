from django.db import models
from django.utils.translation import gettext_lazy as _


class AnswerStatus(models.TextChoices):
    """
        AnswerStatus model is a helper for answer model, representing the status of an answer.

        Attributes:
            CORRECT (str, str): Constant for a correct answer.
            FAULT (str, str): Constant for a faulty answer.

        Relations:
            None
    """

    CORRECT = "correct", _("Correct")
    FAULT = "fault", _("Fault")

