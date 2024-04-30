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
from channel_subscriber.api.serializers.class_room import ClassSerializer
from channel_subscriber.api.serializers.lesson import LessonSerializer
from channel_subscriber.api.serializers.lesson_create import LessonCreateSerializer
from channel_subscriber.api.serializers.lesson_update import LessonUpdateSerializer
from channel_subscriber.models import Lesson
from core.models import Teacher

class ClassLessonViewSet(GenericViewSet, ListModelMixin):
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultLimitOffSetPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return LessonSerializer


    def get_queryset(self):
        class_id = self.kwargs.get("class_pk")
        return Lesson.objects.get_lessons_with_relateds().filter(class_room_id = class_id)