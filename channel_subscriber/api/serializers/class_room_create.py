from django.utils import timezone
from rest_framework import serializers
from channel_subscriber.models import Class
from core.models import Assistant, Teacher, Student
from core.api.serializers.assistant import AssistantSerializer
from core.api.serializers.teacher import TeacherSerializer

class ClassCreateSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(read_only=True)
    assistant = AssistantSerializer(read_only=True, allow_null = True)
    teacher_id = serializers.IntegerField(write_only=True)
    assistant_id = serializers.IntegerField(write_only=True, allow_null=True)
    students = serializers.CharField(write_only=True, allow_null=True, required=False)
    class Meta:
        model = Class
        fields = ["id", "name", "students", "teacher", "assistant", "teacher_id", "assistant_id", "time_start", "time_end"]

    def validate_students(self, attrs):
        def is_comma_separated(input_string):
            comma_count = input_string.count(",")
            return comma_count > 0 and input_string.endswith(",")
        if attrs == None:
            return attrs
        tags = attrs.strip()
        tags = tags.split(",")
        valid_tags = [int(tag.strip()) for tag in tags if tag.strip().isdigit() and tag.strip()]
        # Check if the last element is an empty string and remove it
        if tags and tags[-1].strip() == '':
            tags.pop()

        if valid_tags and is_comma_separated(attrs) and len(tags) == len(valid_tags):
            students = Student.objects.filter(id__in=valid_tags)
            if students.count() == len(valid_tags):
                return students
            else:
                raise serializers.ValidationError({
                    "Error": "You should enter a valid ids for students, these ids not exits and valid."
                })
        else:
            raise serializers.ValidationError({
                "Error": "You should enter a valid string with numbers separated by commas and ending with a comma."
            })
        
    def create(self, validated_data):
        name = validated_data.get("name")
        students = validated_data.get("students")
        teacher_id = validated_data.get("teacher_id")
        assistant_id = validated_data.get("assistant_id")
        time_start = validated_data.get("time_start")
        time_end = validated_data.get("time_end")

        if teacher_id:
            teacher = Teacher.objects.filter(pk=teacher_id).first()
            if not teacher:
                raise serializers.ValidationError({"Error": "this teacher is not exits with this id"})
        
        assistant = None
        if assistant_id:
            assistant = Assistant.objects.filter(pk=assistant_id).first()
            if not assistant:
                raise serializers.ValidationError({"Error": "this assistant is not exits with this id"})
            
        if not students:
            
            class_room = Class()
            class_room.name = name
            class_room.teacher = teacher
            class_room.assistant = assistant
            class_room.time_start = time_start
            class_room.time_end = time_end
            class_room.created_at= timezone.now()
            class_room.save()

            return class_room

        else:

            class_room = Class()
            class_room.name = name
            class_room.teacher = teacher
            class_room.assistant = assistant
            class_room.time_start = time_start
            class_room.time_end = time_end
            class_room.save()
            class_room.students.set(students)

            return class_room

    