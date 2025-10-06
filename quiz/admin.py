from django.contrib import admin
from .models import Quiz, Question, Choice, QuizAttempt, CourseItem,QuizProgress
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.translation import gettext_lazy as _

# Register your models here.

class CourseItemInline(GenericTabularInline):
    model = CourseItem
    extra = 0  # Number of empty forms to display by default
    verbose_name = _("Course Item")
    verbose_name_plural = _("Course Items")

    # Optionally, you can limit which models are shown in the inline:
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('content_object')


class CourseItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'content_type', 'object_id')
    list_filter = ('content_type',)
    search_fields = ('content_type__model', 'object_id')

    class Meta:
        verbose_name = _("Course Item")
        verbose_name_plural = _("Course Items")

    

admin.site.register(CourseItem, CourseItemAdmin)



@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'course_section')
    search_fields = ('id', 'title')
    list_filter = ('title', 'course_section')

    def course_title(self, obj):
        return obj.course.title
    # course_title.admin_order_field = 'course__title'
    # course_title.short_description = 'Course Title'

    def has_module_permission(self, request):
        return request.user.has_perm('quiz.view_quiz') or request.user.is_staff

    def has_view_permission(self, request, obj=None):
        return request.user.has_perm('quiz.view_quiz') or request.user.is_staff
    
   

    def has_view_permission(self, request, obj=None):
        return request.user.has_perm('quiz.view_quiz') or request.user.is_staff

    def has_add_permission(self, request):
        return request.user.has_perm('quiz.add_quiz') or request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.has_perm('quiz.change_quiz') or request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.has_perm('quiz.delete_quiz') or request.user.is_staff
    
    class Meta:
        verbose_name = _("Quiz")
        verbose_name_plural = _("Quizzes")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'quiz', 'text')
    search_fields = ('text', 'quiz__title')
    list_filter = ('quiz',)

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'text', 'is_correct')
    search_fields = ('text', 'question__text')
    list_filter = ('is_correct', 'question')

    class Meta:
        verbose_name = _("Choice")
        verbose_name_plural = _("Choices")


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'quiz', 'score',)
    search_fields = ('user__username', 'quiz__title')
    list_filter = ('quiz',)

    class Meta:
        verbose_name = _("Quiz Attempt")
        verbose_name_plural = _("Quiz Attempts")


@admin.register(QuizProgress)
class QuizProgressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'quiz', 'last_updated')
    search_fields = ('user__username', 'quiz__title')
    list_filter = ('quiz', 'last_updated')

    class Meta:
        verbose_name = _("Quiz Progress")
        verbose_name_plural = _("Quiz Progresses")
