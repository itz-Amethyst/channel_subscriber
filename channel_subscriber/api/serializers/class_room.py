from rest_framework import serializers
from channel_subscriber.models import Class
from core.api.serializers.assistant import AssistantSerializer
from core.api.serializers.teacher import TeacherSerializer
from core.api.serializers.user import UserSerializer

class ClassSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    assistant = AssistantSerializer()
    class Meta:
        model = Class
        fields = ["id", "name", "teacher", "assistant", "time_start", "time_end"]

