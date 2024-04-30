from rest_framework import serializers
from channel_subscriber.models import Lesson, Class
from channel_subscriber.api.serializers.class_room import ClassSerializer
from core.api.serializers.teacher import TeacherSerializer
from core.models import Teacher, Assistant, Student
import os


class LessonCreateSerializer(serializers.ModelSerializer):
    class_room_id = serializers.IntegerField(write_only=True)
    class_room = ClassSerializer(read_only=True)
    teacher = TeacherSerializer(read_only=True)
    class Meta:
        model = Lesson
        fields = ["id", "teacher", "class_room", "class_room_id", "name", "text", "file", "created_at"]


    def validate_file(self, attrs):
        file = attrs
        allowed_extensions = ['.png', '.jpg', '.jpeg', ".pdf"]
        max_size_file = 20 
        # get the extention of avatar
        ext = os.path.splitext(file.name)[1].lower()
        if ext not in allowed_extensions:
            allowed_formats = ', '.join(allowed_extensions)
            error_message = f"Only {allowed_formats} files are allowed."
            raise serializers.ValidationError(
                {
                    "Error":
                     error_message
                }
                                            )
        
        if file.size > (max_size_file * 1024 * 1024):  # Convert megabytes to bytes
            error_message = f"File size should be up to {max_size_file} MB."
            raise serializers.ValidationError({"Error": error_message})
        else:
            return attrs

    def create(self, validated_data):
        breakpoint()
        user_id = self.context.get("user").id
        class_room_id = validated_data.get("class_room_id")
        teacher = Teacher.objects.filter(user__id=user_id).first()
        class_room = Class.objects.filter(pk=class_room_id).first()
        if teacher and class_room:
            name = validated_data.get("name")
            text = validated_data.get("text")
            file = validated_data.get("file")
            lesson = Lesson()
            lesson.teacher = teacher
            lesson.class_room = class_room
            lesson.name = name
            lesson.text = text
            lesson.file = file
            lesson.save()

            return lesson
        else:
            raise serializers.ValidationError({"Error": "There is no teacher or class with these ids"})
        


        