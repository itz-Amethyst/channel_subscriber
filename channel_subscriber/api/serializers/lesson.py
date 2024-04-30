from rest_framework import serializers
from channel_subscriber.models import Lesson
from channel_subscriber.api.serializers.class_room import ClassSerializer
from core.api.serializers.teacher import TeacherSerializer



class LessonSerializer(serializers.ModelSerializer):
    class_room = ClassSerializer(read_only=True)
    teacher = TeacherSerializer(read_only=True)
    class Meta:
        model = Lesson
        fields = ["id", "teacher", "class_room", "name", "text", "file", "created_at"]

        