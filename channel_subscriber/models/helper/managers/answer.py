from django.db import models

class AnswerQuerySet(models.QuerySet):
    def faults(self):
        """
        Returns a queryset of all answers marked as 'fault'.
        """
        return self.filter(status='fault')

    def corrects(self):
        """
        Returns a queryset of all answers marked as 'correct'.
        """
        return self.filter(status='correct')

class AnswerManager(models.Manager):
    def get_queryset(self):
        """
        Returns the custom queryset for the Answer model.
        """
        return AnswerQuerySet(self.model, using=self._db)

    def faults(self):
        """
        Returns a queryset of all answers marked as 'fault'.
        """
        return self.get_queryset().faults()

    def corrects(self):
        """
        Returns a queryset of all answers marked as 'correct'.
        """
        return self.get_queryset().corrects()