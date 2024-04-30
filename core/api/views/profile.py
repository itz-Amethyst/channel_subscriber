from rest_framework.mixins import ListModelMixin , CreateModelMixin , RetrieveModelMixin , DestroyModelMixin , \
    UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from core.api.serializers.profile import ProfileSerializer
from core.api.serializers.profile_update import UpdateProfileSerializer
from core.models.profile import Profile


class ProfileViewSet(GenericViewSet , ListModelMixin , RetrieveModelMixin , UpdateModelMixin ,):
    permission_classes = [IsAuthenticated]
    # pagination_class = DefaultLimitOffSetPagination

    def get_serializer_class( self ):
        if self.request.method == "GET":
            return ProfileSerializer
        elif self.request.method in ["PUT" , "PATCH"]:
            return UpdateProfileSerializer

    def get_queryset( self ):
        return Profile.objects.all()

    def list( self , request , *args , **kwargs ):
        if request.user.is_staff:

            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page , many = True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset , many = True)
            return Response(serializer.data)
        else:
            return Response(
                {"Error": "You cannot list the profiles. Only admins can."} ,
                status = status.HTTP_403_FORBIDDEN ,
            )

    def retrieve( self , request , *args , **kwargs ):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


    def update( self , request , *args , **kwargs ):
        user = self.request.user
        profile = Profile.objects.filter(user_id = user.id).first()
        if profile or user.is_staff == True:
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
        else:
            return Response({"Error": 'You can not update a profile only the main user or admin can'} ,
                            status = status.HTTP_403_FORBIDDEN)
