from rest_framework import serializers
from channel_subscriber.models import Question, Lesson
from core.models import Teacher, Assistant, User
from channel_subscriber.api.serializers.lesson import LessonSerializer
from core.api.serializers.teacher import TeacherSerializer
from core.api.serializers.assistant import AssistantSerializer
from channel_subscriber.api.serializers.helper.delete_image import delete_image
import os


class QuestionUpdateSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(read_only=True)
    assistant = AssistantSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)
    class Meta:
        model = Question
        fields = ["id", "teacher", "assistant", "lesson", "name", "text", "file", "created_at", "expire_time"]



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

    def update(self, instance, validated_data):
        file = validated_data.get("file")
        user_id = self.context.get("user").id
        teacher = Teacher.objects.filter(user__id=user_id).first()
        if teacher and file:
            name = validated_data.get("name")
            text = validated_data.get("text")
            expire_time = validated_data.get("expire_time")
            question = instance
            question.name = name
            delete_image(question.file)
            question.file = file
            question.text = text
            question.expire_time = expire_time
            question.save()

            return question
        elif teacher and not file:
            name = validated_data.get("name")
            text = validated_data.get("text")
            expire_time = validated_data.get("expire_time")
            question = instance
            question.name = name
            question.text = text
            question.expire_time = expire_time
            question.save()

            return question