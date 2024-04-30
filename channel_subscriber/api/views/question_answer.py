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
from channel_subscriber.api.serializers.answer import AnswerSerializer
from channel_subscriber.api.serializers.answer_create import AnswerCreateSerializer
from channel_subscriber.api.serializers.answer_update import AnswerUpdateSerializer
from channel_subscriber.models import Lesson, Question, Answer
from core.models import Teacher, Student, Assistant





class QuestionAnswerViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin):
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        return Answer.objects.filter(question_id=self.kwargs.get("question_pk"))
    

    def get_serializer_class(self):
        if self.request.method == "GET":
            return AnswerSerializer
        elif self.request.method == "POST":
            return AnswerCreateSerializer
        
        elif self.request.method in ["PUT", "PATCH"]:
            return AnswerUpdateSerializer
        


    def list(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_staff == True:
            return super().list(request, *args, **kwargs)
        else:
            return Response({"Error": "You can not perform this action"}, status=status.HTTP_403_FORBIDDEN)
        

    def retrieve(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_staff == True:
            return super().retrieve(request, *args, **kwargs)
        else:
            return Response({"Error": "You can not perform this action"}, status=status.HTTP_403_FORBIDDEN)
        
    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_staff == True:
            return super().update(request, *args, **kwargs)
        else:
            return Response({"Error": "You can not perform this action"}, status=status.HTTP_403_FORBIDDEN)
        

    def create(self, request, *args, **kwargs):
        user = self.request.user

        is_teacher = Question.objects.filter(teacher__user=user, pk=self.kwargs.get("question_pk")).first()
        if is_teacher:
            return Response({"Error": "You can not add an answer becuase you are the teacher of this "})
        else:
            return super().create(request, *args, **kwargs)
        # return super().list(request, *args, **kwargs)