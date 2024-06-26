from rest_framework.mixins import ListModelMixin , CreateModelMixin , RetrieveModelMixin , DestroyModelMixin , \
    UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from channel_subscriber.api.serializers.channel import ChannelSerializer
from channel_subscriber.api.serializers.channel_create import ChannelCreateSerializer
from channel_subscriber.api.serializers.channel_update import ChannelUpdateSerializer

from channel_subscriber.models import  Channel


class ChannelViewSet(GenericViewSet , ListModelMixin , CreateModelMixin , RetrieveModelMixin , UpdateModelMixin ,
                    DestroyModelMixin):
    permission_classes = [IsAuthenticated]

    def get_serializer_context( self ):
        return {"request": self.request , "user": self.request.user}

    def get_serializer_class( self ):
        if self.request.method == "GET":
            return ChannelSerializer
        elif self.request.method == "POST":
            return ChannelCreateSerializer
        elif self.request.method in ["PUT" , "PATCH"]:
            return ChannelUpdateSerializer

    def get_queryset( self ):
        return Channel.objects.get_channels_with_owners().all()


    def retrieve( self , request , *args , **kwargs ):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


    def create( self , request , *args , **kwargs ):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data , status = status.HTTP_201_CREATED , headers = headers)

    def update( self , request , *args , **kwargs ):
        partial = kwargs.pop('partial' , False)
        instance = self.get_object()
        serializer = self.get_serializer(instance , data = request.data , partial = partial)
        serializer.is_valid(raise_exception = True)
        self.perform_update(serializer)

        if getattr(instance , '_prefetched_objects_cache' , None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy( self , request , *args , **kwargs ):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status = status.HTTP_204_NO_CONTENT)