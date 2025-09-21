from django.shortcuts import render,get_object_or_404
from quiz.models import CourseItem
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Blogs, Course , Tutor,Article, CourseSection,Lecture,LectureProgress
from account.decorators import unauthenticated_user,allowed_users
from django.db.models import Prefetch
from quiz.models import Quiz
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CourseSerializer
from django.db.models import Q
from .decorators import course_access_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
from django.http import JsonResponse
from quiz.models import Quiz, Question, Choice, QuizAttempt, UserAnswer,QuizProgress

# Create your views here.



def index(request):
    blogs = Blogs.objects.filter(page_type__name='basic_page')
    hero_section = blogs.filter(blog_type__name='online_platform_education').first()
    global_education = blogs.filter(blog_type__name='global_education').first()
    top_course = blogs.filter(blog_type__name='top_course').first()
    becoming_tutor = blogs.filter(blog_type__name='becoming_a_tutor').first()


    course = Course.objects.filter(is_published=True).filter(is_preview=True)[:3]
    tutors = Tutor.objects.all()[:4]
    articles = Article.objects.all()[:3]

    context = {
        'hero_section': hero_section,
        'global_education': global_education,
        'top_course': top_course,
        'becoming_a_tutor': becoming_tutor,
        'courses': course,
        'tutors': tutors,
        'articles': articles,

    }
    return render(request, 'index.html',context)


def login(request):
    return render(request,'account/login.html')

def popular_courses(request):
    courses = Course.objects.filter(is_published=True).filter(rating__gte=4.5)[:12]
    context = {
        'courses': courses,
    }
    return render(request, 'course/courses.html',context)


def contact(request):
    return render(request, 'contact.html')

#chalasi bor
def team(request):
    tutors = Tutor.objects.all()[:8]
    context ={
        'tutors':tutors
    }
    return render(request, 'team.html',context)

def team_details(request,id):
    tutor = Tutor.objects.get(id=id)
    courses = Course.objects.filter(is_preview=True)[:3]
    
    context = {
        'tutor':tutor,
        'courses':courses
    } 
    return render(request, 'team-details.html',context)

def about(request):
    blog = Blogs.objects.filter(page_type__name='about_page')
    global_education = blog.filter(blog_type__name='global_education').first()
    expert_instruktor = blog.filter(blog_type__name='expert_instruktor').first()
    apply_for_tutor = blog.filter(blog_type__name='apply_for_tutor').first()

    tutors = Tutor.objects.all()[:8]
    context ={
        'tutors':tutors,
        'blog':global_education,
        'expert_instruktor':expert_instruktor,
        'apply_for_tutor':apply_for_tutor,
    }
    return render(request, 'about.html',context)


@api_view(['GET'])
def course_detail(request, id):
    course = get_object_or_404(Course.objects.prefetch_related('sections'), id=id)
    serializer = CourseSerializer(course)
    return Response(serializer.data)


@login_required(login_url='login')
@course_access_required
def lecture(request, id):
    course = get_object_or_404(Course, id=id)

    sections = []
    for section in course.sections.all():  # use related_name='sections' in CourseSection
        items_qs = CourseItem.objects.filter(section=section).select_related('content_type').order_by('order')

        # Filter out orphans & duplicates
        seen_ids = set()
        valid_items = []
        for item in items_qs:
            model_class = item.content_type.model_class() if item.content_type else None
            if not model_class:
                continue
            if not model_class.objects.filter(pk=item.object_id).exists():
                continue  # orphan
            if (item.content_type_id, item.object_id) in seen_ids:
                continue  # duplicate
            seen_ids.add((item.content_type_id, item.object_id))
            valid_items.append(item)

        section.items = valid_items
        sections.append(section)
    
    
    lecture_ids = []
    for section in sections:
        for item in section.items:
            if item.content_type.model == "lecture":
                lecture_ids.append(item.object_id)

    # Fetch last progress only among those lectures
    last_progress = (
        LectureProgress.objects
        .filter(user=request.user, lecture_id__in=lecture_ids)
        .order_by("-updated_at")
        .first()
    )

    if last_progress:
        default_lecture = last_progress.lecture
    else:
        default_lecture = Lecture.objects.filter(id__in=lecture_ids).first()

    

    
    context ={
        'course': course,
        'sections': sections
    }
    context["default_lecture"] = default_lecture
    

    return render(request, 'course/lecture.html', context)




@login_required(login_url='login')
def clear_course_item(request):
    invalid_items = []

    for ci in CourseItem.objects.all():
        model_class = ci.content_type.model_class() if ci.content_type else None
        if not model_class:
            # ContentType row missing
            invalid_items.append(ci)
            continue
        
        if not model_class.objects.filter(pk=ci.object_id).exists():
            # Related object missing
            invalid_items.append(ci)

    # Delete them
    for ci in invalid_items:
        print(f"Deleting: {ci}")
        ci.delete()
    return render(request, 'course/quiz.html')




def find_program(request):
    blog = Blogs.objects.filter(page_type__name='find_program_page')
    blog2 = Blogs.objects.filter(page_type__name='about_page')
    top_tutor = blog.filter(blog_type__name='top_tutors').first()
    apply_for_tutor = blog2.filter(blog_type__name='apply_for_tutor').first()
    context = {
        'top_tutor':top_tutor,
        'apply_for_tutor':apply_for_tutor,
    }
    return render(request, 'find-program.html',context)

def program_details(request,id):
    find_program = {
        '1': {
            'page_type': 'program_detail_page',
            'blog_type': 'sertificates',
            'blog_type1': 'additional_courses_part1',
            'blog_type2': 'additional_courses_part2',
        }
    }
    blog = Blogs.objects.filter(page_type__name=find_program[str(id)]['page_type'])
    sertificates = blog.filter(blog_type__name=find_program[str(id)]['blog_type']).first()
    additional_courses_part1 = blog.filter(blog_type__name=find_program[str(id)]['blog_type1']).first()
    additional_courses_part2 = blog.filter(blog_type__name=find_program[str(id)]['blog_type2']).first()
   

    context = {
        'sertificates':sertificates,
        'additional_courses_part1':additional_courses_part1,
        'additional_courses_part2':additional_courses_part2,
    }
    return render(request, 'program-details.html',context)

def course_details(request,id):
    return render(request, 'course/course-details.html')

def event_details(request,id):
    return render(request, 'event-details.html')

def become_tutor(request):
    return render(request, 'become-tutor.html')

def blog_details(request,id):
    return render(request, 'blog-details.html')

def course_details_v2(request,id):
    return render(request, 'course/course-details-free.html')




def search(request):
    query = request.GET.get('q', '')
    if query:
        courses = Course.objects.filter(is_published=True).filter(Q(title__icontains=query)|Q(course_type__icontains=query)|Q(tags__icontains=query))
    else:
        courses = Course.objects.filter(is_published=True)

    paginator = Paginator(courses, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'courses': page_obj,
    }
    return render(request, 'course/search_course.html',context)


@csrf_exempt
@login_required
def save_answer_and_progress(request, id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    quiz = get_object_or_404(Quiz, id=id)
    data = json.loads(request.body)
    answers = data.get("answers", {})

    # ✅ Count attempts
    attempts_count = QuizAttempt.objects.filter(user=request.user, quiz=quiz).count()
    if attempts_count >= 3:   # max attempts
        return JsonResponse({"error": "Max attempts reached"}, status=403)

    # ✅ Always create new attempt
    attempt = QuizAttempt.objects.create(
        user=request.user,
        quiz=quiz,
        score=0,
        completed_test=False,
        started_at=timezone.now()
    )

    # ✅ Save all answers
    for qid, cid in answers.items():
        question = get_object_or_404(Question, id=qid, quiz=quiz)
        choice = get_object_or_404(Choice, id=cid, question=question)
        UserAnswer.objects.create(
            attempt=attempt,
            question=question,
            chosen_option=choice
        )

    # ✅ Calculate score for this attempt
    correct_count = UserAnswer.objects.filter(
        attempt=attempt, chosen_option__is_correct=True
    ).count()
    attempt.score = (correct_count / quiz.questions.count()) * 100 if quiz.questions.exists() else 0
    attempt.completed_test = True
    attempt.finished_at = timezone.now()
    attempt.save()

    return JsonResponse({
        "status": "ok",
        "score": attempt.score,
        "attempt_number": attempts_count + 1,   # which attempt this is
    })