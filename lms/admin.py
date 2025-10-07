import nested_admin
from django.contrib import admin
from .models import Article, Qualification, CourseSection, CourseBulletPoint, Blogs, Tutor, Course, Review, Lecture,PageType, BlogType
from quiz.models import Quiz, Question, Choice,CourseItem

from django.utils.translation import gettext_lazy as _

from .forms import CourseAdminForm

# Register CourseSection and Lecture explicitly
@admin.register(CourseSection)
class CourseSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
    search_fields = ('title', 'course__title')
    list_filter = ('course__title', 'order')
    exclude = ('order',)

    class Meta:
        verbose_name = _("Course Section")
        verbose_name_plural = _("Course Sections")

@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('id', 'section', 'title', 'video_url', 'duration')
    search_fields = ('id', 'section', 'title', 'video_url')
    list_filter = ('section__course__title', 'section__title')

    class Meta:
        verbose_name = _("Lecture")
        verbose_name_plural = _("Lectures")
# Register Course with nested inlines
class ChoicesInline(nested_admin.NestedStackedInline):
    model = Choice
    extra = 1

    verbose_name = _("Choice")
    verbose_name_plural = _("Choices")

class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    extra = 1
    inlines = [ChoicesInline]

    verbose_name = _("Question")
    verbose_name_plural = _("Questions")

class LectureInline(nested_admin.NestedStackedInline):
    model = Lecture
    extra = 1
    fields = ('id', 'title', 'video_url', 'duration')
    readonly_fields = ('id',)

    verbose_name = _("Lecture")
    verbose_name_plural = _("Lectures")
# class LectureInline(nested_admin.NestedTabularInline):
#     model = Lecture
#     extra = 1

# class CourseItemInline(nested_admin.NestedStackedInline):
#     model = CourseItem
#     extra = 1

class ReviewInline(nested_admin.NestedStackedInline):
    model = Review
    extra = 1

    verbose_name = _("Review")
    verbose_name_plural = _("Reviews")




class QuizInline(nested_admin.NestedStackedInline):
    model = Quiz
    extra = 1
    inlines = [QuestionInline]
    exclude = ('order',)

    verbose_name = _("Quiz")
    verbose_name_plural = _("Quizzes")

class CourseSectionInline(nested_admin.NestedStackedInline):
    model = CourseSection
    extra = 1
    inlines = [LectureInline,QuizInline]
    exclude = ('order',)

    verbose_name = _("Course Section")
    verbose_name_plural = _("Course Sections")

@admin.register(Course)
class CourseAdmin(nested_admin.NestedModelAdmin):
    form = CourseAdminForm
    list_display = ('title', 'course_type', 'tutor', 'rating', 'student_count', 'price')
    search_fields = ('title', 'tags', 'course_type')
    list_filter = ('course_type', 'tutor')
    inlines = [CourseSectionInline,ReviewInline]

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")

# Other model registrations
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'organiser_full_name', 'organiser_email', 'created_at')
    search_fields = ('title', 'description', 'category', 'topic', 'organiser_full_name', 'organiser_email', 'organiser_phone')
    list_filter = ('created_at', 'category')

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")

@admin.register(Blogs)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'page_type', 'blog_type', 'vimeo_url')
    search_fields = ('title', 'page_type', 'blog_type', 'vimeo_url', 'description')
    list_filter = ('page_type', 'blog_type')

    class Meta:
        verbose_name = _("Blog")
        verbose_name_plural = _("Blogs")

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', )
    list_filter = ('name',)

    class Meta:
        verbose_name = _("Blog Type")
        verbose_name_plural = _("Blog Types")

@admin.register(PageType)
class PageTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', )
    list_filter = ('name',)


    class Meta:
        verbose_name = _("Page Type")
        verbose_name_plural = _("Page Types")



@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'institution')
    search_fields = ('title', 'institution')
    list_filter = ('institution',)

    class Meta:
        verbose_name = _("Qualification")
        verbose_name_plural = _("Qualifications")

class QualificationInline(nested_admin.NestedStackedInline):
    model = Qualification
    extra = 1

    verbose_name = _("Qualification")
    verbose_name_plural = _("Qualifications")

class CourseInline(nested_admin.NestedStackedInline):
    model = Course
    extra = 1
    verbose_name = _("Course")
    verbose_name_plural = _("Courses")

@admin.register(Tutor)
class TutorAdmin(nested_admin.NestedModelAdmin):
    list_display = ('name', 'subject', 'experience_years', 'hourly_rate')
    search_fields = ('name', 'subject', 'description', 'experience_years')
    inlines = [QualificationInline,CourseInline]

    class Meta:
        verbose_name = _("Tutor")
        verbose_name_plural = _("Tutors")



admin.site.register(CourseBulletPoint)
