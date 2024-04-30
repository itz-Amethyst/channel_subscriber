from django.db import models
from django.utils.translation import gettext_lazy as _
class PathOptions(models.TextChoices):
    """
    PathOptions model is a helper for models which have upload field in it, representing the path of a file.

    Attributes:
        LESSONS (str): Constant for lessons.
        ANSWERS (str): Constant for answers.
        QUESTIONS (str): Constant for questions.
        OTHERS (str): Constant for other values.
    """

    LESSONS = "lessons" , _("Lessons")
    ANSWERS = "answers" , _("Answers")
    QUESTIONS = "questions" , _("Questions")
    OTHERS = "others" , _("Others")

    def __str__(self):
        return str(self.value)

    @classmethod
    def choices(cls):
        return [(path.name, path.value) for path in cls]