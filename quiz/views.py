from django.shortcuts import render, get_object_or_404
from .models import Quiz, Question, Choice, QuizAttempt,UserAnswer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    QuizSerializer,
    QuestionSerializer,
    ChoiceSerializer,
    QuizAttemptSerializer,
    UserAnswerSerializer,
)

@login_required(login_url='login')
def quiz(request,id):
    quizes = Quiz.objects.get(id=id)
    context ={
        'quizes': quizes
    }
    return render(request, 'course/quiz.html',context)

@login_required(login_url='login')
def quiz_page(request, id):
    quiz = get_object_or_404(Quiz, id=id)
    print(quiz.questions)
    context = {
        'quiz_id': quiz.id,
        'quiz_title': quiz.title,
    }
    return render(request, 'course/quiz2.html', context)

@login_required
def get_quiz_data(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = []
    for q in quiz.questions.all():
        questions.append({
            'id': q.id,
            'text': q.text,
            'choices': [{'id': c.id, 'text': c.text} for c in q.choices.all()]
        })
    return JsonResponse({'quiz': quiz.title, 'questions': questions})

@csrf_exempt  # for testing — use CSRF token in production!
@login_required
def submit_quiz(request, quiz_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        quiz = get_object_or_404(Quiz, id=quiz_id)
        score = 0
        total = quiz.questions.count()

        for q in quiz.questions.all():
            user_answer = str(data.get(str(q.id)))
            correct = q.choices.filter(is_correct=True).first()
            if correct and user_answer == str(correct.id):
                score += 1

        percentage = (score / total) * 100 if total > 0 else 0

        QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=percentage
        )

        return JsonResponse({
            'score': score,
            'total': total,
            'percentage': percentage
        })

# ViewSet for quizzes. This will provide all CRUD (Create, Read, Update, Delete) operations.
# We'll use a `ReadOnlyModelViewSet` as a basic example, but you could use a full `ModelViewSet`
# if you wanted an API to create/edit quizzes.
class QuizViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows quizzes to be viewed.
    It returns a list of all quizzes and a single quiz with its nested questions and choices.
    """
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]


# A ViewSet for questions. We're using ReadOnlyModelViewSet because questions
# will primarily be retrieved as part of a quiz, not individually created/updated via this endpoint.
class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows questions to be viewed.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]


# A ViewSet for quiz attempts. This is a critical view for managing a user's progress.
# This ViewSet will handle creating new attempts, retrieving an existing attempt, and
# updating an attempt (e.g., when a user finishes).
class QuizAttemptViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows quiz attempts to be viewed or created.
    """
    queryset = QuizAttempt.objects.all()
    serializer_class = QuizAttemptSerializer
    permission_classes = [IsAuthenticated]

    # This method ensures that users can only see their own quiz attempts.
    def get_queryset(self):
        return QuizAttempt.objects.filter(user=self.request.user).order_by('-started_at')

    # This method automatically sets the user on the quiz attempt when it's created.
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# A ViewSet for user answers. A user will create a new UserAnswer for each question they answer.
# We use ModelViewSet here to allow creating (POST) and updating (PUT/PATCH) answers.
class UserAnswerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows user answers to be viewed, created, or updated.
    """
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer
    permission_classes = [IsAuthenticated]
    
    # This ensures users can only see and modify their own answers within a quiz attempt.
    def get_queryset(self):
        return UserAnswer.objects.filter(attempt__user=self.request.user)

