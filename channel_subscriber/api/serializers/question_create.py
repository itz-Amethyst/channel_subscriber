from rest_framework import serializers
from channel_subscriber.models import Question, Lesson
from core.models import Teacher, Assistant, User
from channel_subscriber.api.serializers.lesson import LessonSerializer
from core.api.serializers.teacher import TeacherSerializer
from core.api.serializers.assistant import AssistantSerializer
import os


class QuestionCreateSerializer(serializers.ModelSerializer):
    assistant_id = serializers.IntegerField(write_only=True, allow_null=True, required=False)
    lesson_id = serializers.IntegerField(write_only=True)
    teacher = TeacherSerializer(read_only=True)
    assistant = AssistantSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)
    class Meta:
        model = Question
        fields = ["id", "teacher", "assistant", "assistant_id", "lesson", "lesson_id", "name", "text", "file", "created_at", "expire_time"]



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
        user_id = self.context.get("user").id
        assistant_id = validated_data.get("assistant_id")
        lesson_id = validated_data.get("lesson_id")
        teacher = Teacher.objects.filter(user__id=user_id).first()
        assistant = Assistant.objects.filter(pk=assistant_id).first()
        lesson = Lesson.objects.filter(pk=lesson_id).first()
        if teacher and assistant and lesson:
            name = validated_data.get("name")
            text = validated_data.get("text")
            file = validated_data.get("file")
            expire_time = validated_data.get("expire_time")
            question = Question()
            question.teacher = teacher
            question.assistant = assistant
            question.lesson = lesson
            question.name = name
            question.file = file
            question.text = text
            question.expire_time = expire_time
            question.save()

            return question
        elif teacher and lesson:
            name = validated_data.get("name")
            text = validated_data.get("text")
            file = validated_data.get("file")
            expire_time = validated_data.get("expire_time")
            question = Question()
            question.teacher = teacher
            question.lesson = lesson
            question.name = name
            question.file = file
            question.text = text
            question.expire_time = expire_time
            question.save()

            return question
        else:
            raise serializers.ValidationError({"Error": "There is no teacher or assistant or lesson with these ids"})
        

