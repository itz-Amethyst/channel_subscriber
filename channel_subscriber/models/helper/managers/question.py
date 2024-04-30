from django.db import models
from django.utils import timezone

current_time = timezone.now()

class QuestionManager(models.Manager):

    def get_queryset(self, include_expired = False):
        """
        Overrides the default queryset to filter out expired questions.
        """
        queryset = super(QuestionManager, self).get_queryset()
        if not include_expired:
            return queryset.filter(expire_time__gte=current_time)
        return queryset
    def get_expired_questions(self) -> dict:
        """
        Returns a dictionary of all expired questions.

        Returns:
            dict: A dictionary where keys are question IDs and values are corresponding expired Question objects.
        """
        expired_questions = {}

        for question in self.get_queryset(include_expired = True):
            if question.expire_time < current_time:
                expired_questions[question.id] = question

        return expired_questions

    def get_questions_with_all_relateds( self ):
        """
            Retrieves all questions with related fields pre-fetched.

            Returns:
                QuerySet: QuerySet containing all questions with related fields pre-fetched.
        """
        return super().get_queryset().select_related(
            "teacher__user" ,
            "lesson__teacher__user" ,
            "lesson__class_room__teacher__user" ,
            "assistant__student__user" ,
            "assistant__teacher__user"
        )