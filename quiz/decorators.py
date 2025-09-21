from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from .models import QuizAttempt, Quiz

def limit_attempts(max_attempts=3):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, id, *args, **kwargs):
            quiz = Quiz.objects.get(id=id)
            attempt_count = QuizAttempt.objects.filter(user=request.user, quiz=quiz).count()

            if attempt_count >= max_attempts:
                messages.warning(
                    request,
                    f"⚠️ You have already attempted this quiz {max_attempts} times. Showing your results instead."
                )
                return redirect("quiz_results", id=quiz.id)  # 👈 send them to results view

            return view_func(request, id, *args, **kwargs)
        return _wrapped_view
    return decorator
