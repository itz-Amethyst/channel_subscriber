from rest_framework.mixins import ListModelMixin , CreateModelMixin , RetrieveModelMixin , DestroyModelMixin , \
    UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.utils.translation import gettext_lazy as _
from channel_subscriber.api.serializers.subscription import SubscriptionCreateSerializer
from channel_subscriber.api.serializers.unsubscription import SubscriptionDeleteSerializer

from channel_subscriber.models import  Subscription


class SubscriptionViewSet(GenericViewSet , ListModelMixin , CreateModelMixin , RetrieveModelMixin , UpdateModelMixin ,
                    DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    http_method_names = ["post", "delete"]

    def get_serializer_context( self ):
        return {"request": self.request , "user": self.request.user}

    def get_serializer_class( self ):
        if self.request.method == "POST":
            return SubscriptionCreateSerializer
        elif self.request.method == "DELETE":
            return SubscriptionDeleteSerializer

    def get_queryset( self ):
        return Subscription.objects.get_subscriptions_with_users.all()

    def create( self , request , *args , **kwargs ):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data , status = status.HTTP_201_CREATED , headers = headers)

    def destroy( self , request , *args , **kwargs ):
        data = {
            "channel_id": kwargs.get('pk')
        }
        serializer = self.get_serializer(data = data)
        serializer.is_valid(raise_exception = True)  # Ensure the request is valid

        # Unsubscribe by deleting the corresponding Subscription
        subscriber = request.user
        channel = serializer.validated_data["channel_id"]
        target = channel.owner

        # Find the Subscription instance to delete
        subscription = Subscription.objects.filter(subscriber = subscriber , target = target).first()
        if not subscription:
            return Response(
                {"error": _("Subscription not found.")} ,
                status = status.HTTP_404_NOT_FOUND
            )

        subscription.delete()  # Delete the subscription
        return Response(status = status.HTTP_204_NO_CONTENT)  # Return successful deletion