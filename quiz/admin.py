from django.contrib import admin
from .models import Quiz, Question, Choice, QuizAttempt, CourseItem,QuizProgress
from django.contrib.contenttypes.admin import GenericTabularInline

# Register your models here.

class CourseItemInline(GenericTabularInline):
    model = CourseItem
    extra = 0  # Number of empty forms to display by default
    verbose_name = "Course Item"
    verbose_name_plural = "Course Items"

    # Optionally, you can limit which models are shown in the inline:
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('content_object')


class CourseItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'content_type', 'object_id')
    list_filter = ('content_type',)
    search_fields = ('content_type__model', 'object_id')

    

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


admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(QuizAttempt)
admin.site.register(QuizProgress)