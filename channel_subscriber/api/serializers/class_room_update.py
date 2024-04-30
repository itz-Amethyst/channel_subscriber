from rest_framework import serializers
from channel_subscriber.models import Class
from core.models import Student


class ClassUpdateSerializer(serializers.ModelSerializer):
    students = serializers.CharField(write_only=True, allow_null=True, required=False)
    class Meta:
        model = Class
        fields = ["id", "name", "students", "time_start", "time_end"]


    def validate_students(self, attrs):
        def is_comma_separated(input_string):
            comma_count = input_string.count(",")
            return comma_count > 0 and input_string.endswith(",")
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
    def update(self, instance, validated_data):
        students = validated_data.get("students")
        name = validated_data.get("name")
        time_start = validated_data.get("time_start")
        time_end = validated_data.get("time_end")

        class_room = instance
        class_room.students.set(students)
        class_room.name = name
        class_room.time_start = time_start
        class_room.time_end = time_end
        class_room.save()

        return class_room
