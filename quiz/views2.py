# quiz/views2.py
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, Choice, QuizProgress, QuizAttempt, UserAnswer
from django.utils import timezone

@login_required
@csrf_exempt
def start_new_attempt(request, id):
    quiz = get_object_or_404(Quiz, id=id)

    attempts_count = QuizAttempt.objects.filter(user=request.user, quiz=quiz).count()
    if attempts_count >= 3:
        return JsonResponse({"error": "Max attempts reached"}, status=403)

    # block if user has unfinished attempt
    unfinished = QuizAttempt.objects.filter(user=request.user, quiz=quiz, completed_test=False).first()
    if unfinished:
        return JsonResponse({"error": "Finish your current attempt first"}, status=400)

    # create fresh attempt
    attempt = QuizAttempt.objects.create(
        user=request.user,
        quiz=quiz,
        score=0,
        completed_test=False,
        started_at=timezone.now()
    )

    # reset progress
    QuizProgress.objects.filter(user=request.user, quiz=quiz).delete()
    QuizProgress.objects.create(user=request.user, quiz=quiz)

    return JsonResponse({"success": True, "attempt_id": attempt.id, "attempts_count": attempts_count + 1})


@login_required
def get_quiz_with_progress(request, id):
    quiz = get_object_or_404(Quiz, id=id)
    attempts = QuizAttempt.objects.filter(user=request.user, quiz=quiz).order_by('-started_at')
    attempts_count = attempts.count()

    # get active attempt
    active_attempt = attempts.filter(completed_test=False).first()

    if not active_attempt:
        # no ongoing attempt
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
                "answered_questions": [],
                "answered_count": 0,
                "total_questions": quiz.questions.count(),
                "current_question_index": 0,
            },
            "answered_questions_details": [],
            "quiz_is_complete": True,  # ✅ now only true if no active attempt
            "attempts_count": attempts_count,
        })

    # ongoing attempt
    progress, _ = QuizProgress.objects.get_or_create(user=request.user, quiz=quiz)

    user_answers = UserAnswer.objects.filter(attempt=active_attempt)
    answered_questions = [{
        "id": ua.question.id,
        "text": ua.question.text,
        "choices": [{"id": c.id, "text": c.text} for c in ua.question.choices.all()],
        "user_choice_id": ua.chosen_option.id,
    } for ua in user_answers]

    progress.answered_questions = list(user_answers.values_list("question_id", flat=True))
    progress.current_question_index = len(progress.answered_questions)
    progress.save()

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
        "quiz_is_complete": False,  # ✅ because attempt is still open
        "attempts_count": attempts_count,
    })


