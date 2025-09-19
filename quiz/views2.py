# quiz/views2.py
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, Choice, QuizProgress, QuizAttempt, UserAnswer


@login_required
def get_quiz_with_progress(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    progress, _ = QuizProgress.objects.get_or_create(user=request.user, quiz=quiz)

    # Get answered questions for this quiz only
    user_answers = UserAnswer.objects.filter(
        attempt__user=request.user, attempt__quiz=quiz
    )

    answered_questions = []
    for ua in user_answers:
        answered_questions.append({
            "id": ua.question.id,
            "text": ua.question.text,
            "choices": [{"id": c.id, "text": c.text} for c in ua.question.choices.all()],
            "user_choice_id": ua.chosen_option.id,
        })

    # Sync progress with actual answers
    progress.answered_questions = list(user_answers.values_list("question_id", flat=True))
    progress.current_question_index = len(progress.answered_questions)
    progress.save()

    # Remaining questions
    remaining_questions = []
    for q in quiz.questions.exclude(id__in=progress.answered_questions):
        remaining_questions.append({
            "id": q.id,
            "text": q.text,
            "choices": [{"id": c.id, "text": c.text} for c in q.choices.all()],
        })

    return JsonResponse({
        "quiz_info": {
            "title": quiz.title,
            "description": quiz.description,
            "questions": [
                {
                    "id": q.id,
                    "text": q.text,
                    "choices": [{"id": c.id, "text": c.text} for c in q.choices.all()]
                }
                for q in quiz.questions.all()
            ]
        },
        "progress": {
            "answered_questions": progress.answered_questions,
            "answered_count": len(progress.answered_questions),
            "total_questions": quiz.questions.count(),
            "current_question_index": progress.current_question_index,
        },
        "answered_questions_details": answered_questions,
        "remaining_questions": remaining_questions,
        "quiz_is_complete": len(progress.answered_questions) == quiz.questions.count(),
    })


@csrf_exempt
@login_required
def save_answer_and_progress(request, quiz_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    quiz = get_object_or_404(Quiz, id=quiz_id)
    data = json.loads(request.body)

    question = get_object_or_404(Question, id=data.get("question_id"), quiz=quiz)
    choice = get_object_or_404(Choice, id=data.get("choice_id"), question=question)

    # Ensure attempt exists
    attempt, _ = QuizAttempt.objects.get_or_create(
        user=request.user, quiz=quiz, defaults={"score": 0}
    )

    # Save or update UserAnswer
    UserAnswer.objects.update_or_create(
        attempt=attempt,
        question=question,
        defaults={"chosen_option": choice}
    )

    # Update progress based only on answers for this attempt
    answered_ids = list(UserAnswer.objects.filter(attempt=attempt).values_list("question_id", flat=True))
    progress, _ = QuizProgress.objects.get_or_create(user=request.user, quiz=quiz)
    progress.answered_questions = answered_ids
    progress.current_question_index = len(answered_ids)
    progress.save()

    # Recalculate score
    correct_count = UserAnswer.objects.filter(attempt=attempt, chosen_option__is_correct=True).count()
    attempt.score = (correct_count / quiz.questions.count()) * 100 if quiz.questions.exists() else 0
    attempt.save()

    return JsonResponse({
        "status": "ok",
        "question_id": question.id,
        "choice_id": choice.id,
        "is_correct": choice.is_correct,
        "current_score": attempt.score,
    })
