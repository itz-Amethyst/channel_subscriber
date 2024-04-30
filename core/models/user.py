from typing import Dict , List

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from rest_framework_simplejwt.tokens import RefreshToken




class User(AbstractUser):
    """
    User model representing a user in the system.

    Attributes:
        email (models.EmailField): Email field for the user.

    Relations:
        None
    """

    email: models.EmailField = models.EmailField(
        verbose_name=_("Email"),
        help_text=_("This is the email address of the user."),
        db_comment=_("This is the email address of the user."),
        unique=True,
        validators=[validate_email]
    )


    class Meta:
        db_table: str = "users"
        db_table_comment: str = "This table contains all users in the system."
        verbose_name: str = _("User")
        verbose_name_plural: str = _("Users")

        constraints: list = [
            models.CheckConstraint(
                check=models.Q(date_joined__gte=models.ExpressionWrapper(models.Value("NOW()"),
                                                                         output_field=models.DateTimeField())),
                name="check_date_joined",
                violation_error_message=_("The date joined must be in the past or present.")
            ),
            models.CheckConstraint(
                check=models.Q(last_login__gte=models.ExpressionWrapper(models.Value("NOW()"),
                                                                        output_field=models.DateTimeField())),
                name="check_last_login",
                violation_error_message=_("The last login must be in the past or present.")
            ),
            models.CheckConstraint(
                check=models.Q(last_login__gte=models.F('date_joined')),
                name="last_login_after_date_joined",
                violation_error_message=_("The last login must be after the date joined.")
            ),
        ]

    def generate_token( self ):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh) ,
            'access': str(refresh.access_token)
        }


    def save( self , *args: List , **kwargs: Dict ) -> None:
        """
            Override the save method to perform validation before saving.
        """
        self.clean()
        super().save(*args , **kwargs)
