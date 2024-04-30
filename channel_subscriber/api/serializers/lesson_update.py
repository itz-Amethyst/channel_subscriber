from rest_framework import serializers
from channel_subscriber.models import Lesson
from channel_subscriber.api.serializers.class_room import ClassSerializer
from core.api.serializers.teacher import TeacherSerializer
from channel_subscriber.api.serializers.helper.delete_image import delete_image
import os


class LessonUpdateSerializer(serializers.ModelSerializer):
    file = serializers.FileField(allow_null=True, required=False)
    class Meta:
        model = Lesson
        fields = ["id", "name", "text", "file", "created_at"]


    def validate_file(self, attrs):
        file = attrs
        allowed_extensions = ['.png', '.jpg', '.jpeg', ".pdf"]
        max_size_file = 20
        if file == None:
            return attrs 
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
        name = validated_data.get("name")
        text = validated_data.get("text")
        file = validated_data.get("file")
        if file:
            lesson = instance
            delete_image(lesson.file)
            lesson.file = file
            lesson.name = name
            lesson.text = text
            lesson.save()

            return lesson
        else:
            lesson = instance
            lesson.name = name
            lesson.text = text
            lesson.save()

            return lesson
