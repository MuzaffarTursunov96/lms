from functools import wraps
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .models import Course, UserCourses

def course_access_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, id, *args, **kwargs):
        # Get the course or 404 if it doesn't exist
        course = get_object_or_404(Course, id=id)

        # Check if user is authenticated
        if not request.user.is_authenticated:
            return redirect('login')  # Or your login URL name

        # Check if the user is enrolled
        has_access = UserCourses.objects.filter(user=request.user, course=course).exists()

        if not has_access:
            return HttpResponseForbidden("🚫 You don’t have permission to access this course.")

        # If everything is OK → run the view
        return view_func(request, id, *args, **kwargs)

    return _wrapped_view