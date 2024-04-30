from rest_framework import serializers
from channel_subscriber.models import Question, Answer
from core.models import Student, Teacher, Assistant
from channel_subscriber.api.serializers.lesson import LessonSerializer
from core.api.serializers.teacher import TeacherSerializer
from core.api.serializers.assistant import AssistantSerializer
from core.api.serializers.student import StudentSerializer
from channel_subscriber.api.serializers.question import QuestionSerializer

class AnswerCreateSerializer(serializers.ModelSerializer):
    question_id = serializers.IntegerField(read_only=True)
    question = QuestionSerializer(read_only=True)
    student = StudentSerializer(read_only=True)
    class Meta:
        model = Answer
        fields = ["id", "student", "question", "question_id", "name", "text", "file", "created_at"]


    def create(self, validated_data):
        breakpoint()
        user = self.context.get("user")
        student = Student.objects.filter(user=user).first()

        if not student:
            raise serializers.ValidationError({"Error": "this is not a student to add a answer to this question"})
        # return super().create(validated_data)
