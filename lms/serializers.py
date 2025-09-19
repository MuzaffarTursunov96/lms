from rest_framework import serializers
from .models import Lecture,CourseSection, Course
from quiz.models import CourseItem,Quiz

class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['id', 'title', 'video_url', 'duration']

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description']

class CourseItemSerializer(serializers.Serializer):
    type = serializers.CharField()
    lecture = LectureSerializer(required=False)
    quiz = QuizSerializer(required=False)

class SectionSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = CourseSection
        fields = ['id', 'title', 'items']

    def get_items(self, obj):
        items_qs = CourseItem.objects.filter(section=obj).select_related('content_type').order_by('order')

        seen_ids = set()
        valid_items = []
        for item in items_qs:
            print(item,' <<<item')
            model_class = item.content_type.model_class() if item.content_type else None
            if not model_class:
                continue
            if not model_class.objects.filter(pk=item.object_id).exists():
                continue
            if (item.content_type_id, item.object_id) in seen_ids:
                continue
            seen_ids.add((item.content_type_id, item.object_id))

            if item.content_type.model == 'lecture':
                valid_items.append({"type": "lecture", "lecture": LectureSerializer(item.content_object).data})
            elif item.content_type.model == 'quiz':
                valid_items.append({"type": "quiz", "quiz": QuizSerializer(item.content_object).data})

        return valid_items

class CourseSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'sections']
