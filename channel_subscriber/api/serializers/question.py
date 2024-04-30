from rest_framework import serializers
from channel_subscriber.models import Question
from channel_subscriber.api.serializers.lesson import LessonSerializer
from core.api.serializers.teacher import TeacherSerializer
from core.api.serializers.assistant import AssistantSerializer

class QuestionSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    assistant = AssistantSerializer()
    lesson = LessonSerializer()
    class Meta:
        model = Question
        fields = ["id", "teacher", "assistant", "lesson", "name", "text", "file", "created_at"]
