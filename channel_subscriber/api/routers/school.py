from rest_framework_nested import routers
from channel_subscriber.api.views.class_room import ClassViewSet
from channel_subscriber.api.views.class_room_lesson import ClassLessonViewSet
from channel_subscriber.api.views.lesson import LessonViewSet
from channel_subscriber.api.views.question import QuestionViewSet
from channel_subscriber.api.views.question_answer import QuestionAnswerViewSet


router = routers.DefaultRouter()



router.register("classes", ClassViewSet, basename="classes")
router.register("lessons", LessonViewSet, basename="lessons")
router.register("questions", QuestionViewSet, basename="questions")
class_lesson_router = routers.NestedDefaultRouter(router, "classes", lookup="class")
class_lesson_router.register("lessons", ClassLessonViewSet, basename="class-lessons")

question_answer_router = routers.NestedDefaultRouter(router, "questions", lookup="question")
question_answer_router.register("answers", QuestionAnswerViewSet, basename="question-answers")



urlpatterns = router.urls + class_lesson_router.urls + question_answer_router.urls