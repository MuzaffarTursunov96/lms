# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import LectureProgress, Lecture

@csrf_exempt
def save_progress(request):
    if request.method == "POST":
        data = json.loads(request.body)
        video_id = data.get("video_id")
        watched_percent = data.get("watched_percent")
        watched_seconds = data.get("watched_seconds", 0)

        lecture = Lecture.objects.filter(video_id=video_id).first()
        if lecture and request.user.is_authenticated:
            LectureProgress.objects.update_or_create(
                user=request.user,
                lecture=lecture,
                defaults={"watched_percent": watched_percent, "watched_seconds": watched_seconds}
            )
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"})