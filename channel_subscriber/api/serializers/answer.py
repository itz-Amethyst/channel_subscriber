from rest_framework import serializers
from channel_subscriber.models import Question, Answer
from channel_subscriber.api.serializers.lesson import LessonSerializer
from core.api.serializers.teacher import TeacherSerializer
from core.api.serializers.assistant import AssistantSerializer
from core.api.serializers.student import StudentSerializer
from channel_subscriber.api.serializers.question import QuestionSerializer

class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()
    student = StudentSerializer()
    class Meta:
        model = Answer
        fields = ["id", "student", "question", "name", "text", "file", "status", "created_at"]
