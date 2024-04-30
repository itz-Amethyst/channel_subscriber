from django.db import models


class ClassManager(models.Manager):
    def get_classes_with_teachers(self):
        """
        Retrieves all classes with related fields pre-fetched.

        Returns:
            QuerySet: QuerySet containing all classes with related fields pre-fetched.
        """
        return super().get_queryset().select_related("teacher__user")