from django.db import models


#! If the school has multiple section part
class Section(models.Model):
    name = models.CharField(max_length = 50)
    lessons_count = models.IntegerField(default = 0 , editable = False)

    def update_lessons_count( self ):
        self.lessons_count = self.lessons.count()
        self.save()

    def __str__( self ):
        return self.name