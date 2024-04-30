from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from channel_subscriber.models.helper.managers.subscription import SubscriptionManager


class Subscription(models.Model):
    """
    Represents a subscription between users.

    Fields:
        subscriber (ForeignKey): The user who is subscribing.
        target (ForeignKey): The user who is being subscribed to.

    Constraints:
        - A user cannot subscribe to themselves.
        - The combination of subscriber and target must be unique (no duplicate subscriptions).
    """

    subscriber = models.ForeignKey(
        to = settings.AUTH_USER_MODEL ,
        related_name = "subscriptions" ,
        verbose_name = _("Subscriber") ,
        help_text = _("The user who is subscribing.") ,
        db_comment = _("The user who is subscribing.") ,
        on_delete = models.CASCADE ,
    )

    target = models.ForeignKey(
        to = settings.AUTH_USER_MODEL ,
        related_name = "subscribers" ,
        verbose_name = _("Target") ,
        help_text = _("The user who is being subscribed to.") ,
        db_comment = _("The user who is being subscribed to.") ,
        on_delete = models.CASCADE ,
    )

    objects: models.Manager[SubscriptionManager] = SubscriptionManager()

    class Meta:
        db_table = "subscriptions"
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")
        unique_together = ("subscriber" , "target")  # Enforce uniqueness of subscriptions
        constraints = [
            models.CheckConstraint(
                check = ~models.Q(subscriber = models.F("target")) ,
                name = "no_self_subscription" ,
                violation_error_message = _("A user cannot subscribe to themselves.") ,
            ) ,
        ]

    def clean( self ) -> None:
        if self.subscriber == self.target:
            raise ValidationError(_("A user cannot subscribe to themselves."))

        super().clean()

