# your_app_name/serializers.py
from rest_framework import serializers
from .models import Quiz, Question, Choice, QuizAttempt, UserAnswer

# --- Nested Serializers for Quiz retrieval ---

# Serializer for a single Choice
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'is_correct']

# Serializer for a single Question, which includes its Choices
class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'choices']



# Main Quiz Serializer, which includes its Questions and their Choices
class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    total_questions = serializers.ReadOnlyField() # Exposes the total_questions method on the model

    class Meta:
        model = Quiz
        fields = ['id', 'course', 'course_section', 'title', 'description', 'total_questions', 'questions']

# --- Serializers for handling user submissions ---

# Serializer for a single UserAnswer submission
class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = ['id', 'question', 'chosen_option']

# Serializer for a QuizAttempt. This is used when a user starts or finishes a quiz.
class QuizAttemptSerializer(serializers.ModelSerializer):
    user_answers = UserAnswerSerializer(many=True, read_only=True) # Nested field for user's answers

    class Meta:
        model = QuizAttempt
        fields = ['id', 'user', 'quiz', 'score', 'started_at', 'finished_at', 'user_answers']
        read_only_fields = ['user', 'score', 'started_at'] # User and score are set by the view, not the client

# Note: You would likely want a separate, more secure view for creating and grading a QuizAttempt
# This serializer is mainly for displaying the data once it's created.

