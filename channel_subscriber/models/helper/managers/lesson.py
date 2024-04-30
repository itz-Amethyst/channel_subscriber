from django.db import models


class LessonManager(models.Manager):

    def get_is_primaries( self ):
        """
        Retrieves lessons with is_primary set to True.

        Returns:
            QuerySet: QuerySet containing lessons where is_primary is True.
        """
        return super().get_queryset().filter(is_primary = True)

    def get_lessons_with_relateds( self ):
        """
        Retrieves all lessons with related fields pre-fetched.

        Returns:
            QuerySet: QuerySet containing all lessons with related fields pre-fetched.
        """
        return super().get_queryset().select_related("teacher__user" , "class_room__teacher__user")
