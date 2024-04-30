from rest_framework import status
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from core.models import User, Teacher, Student
from core.api.paginations.limit_of_set import DefaultLimitOffSetPagination
from core.api.serializers.teacher_create import TeacherCreateSerializer
from core.api.serializers.teacher import TeacherSerializer
from core.api.serializers.teacher_update import TeacherUpdateSerializer
from core.api.serializers.student import StudentSerializer
from channel_subscriber.api.serializers.lesson import LessonSerializer
from channel_subscriber.api.serializers.lesson_create import LessonCreateSerializer
from channel_subscriber.api.serializers.question import QuestionSerializer
from channel_subscriber.api.serializers.question_create import QuestionCreateSerializer
from channel_subscriber.api.serializers.question_update import QuestionUpdateSerializer
from channel_subscriber.models import Lesson, Question
from core.models import Teacher

class QuestionViewSet(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultLimitOffSetPagination


    def get_serializer_context(self):
        return {"request": self.request, "user": self.request.user}
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return QuestionSerializer
        elif self.request.method == "POST":
            return QuestionCreateSerializer
        else:
            return QuestionUpdateSerializer
        # elif self.request.method == "POST":
        #     return LessonCreateSerializer
        # elif self.request.method in ["PUT", "PATCH"]:
        #     return LessonUpdateSerializer

    def get_queryset(self):
        return Question.objects.get_questions_with_all_relateds().all()
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        teacher = Teacher.objects.filter(user_id=user.id).first()
        if teacher:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({"Error": 'You can not create a lesson only teacher can'}, status=status.HTTP_403_FORBIDDEN)
        

    def update(self, request, *args, **kwargs):
        user = self.request.user
        teacher = Teacher.objects.filter(user_id=user.id).first()
        if teacher:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        else:
            return Response({"Error": 'You can not update a lesson only teacher can'}, status=status.HTTP_403_FORBIDDEN)
        

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        teacher = Teacher.objects.filter(user_id=user.id).first()
        if teacher:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"Error": 'You can not delete a lesson only teacher can'}, status=status.HTTP_403_FORBIDDEN)
