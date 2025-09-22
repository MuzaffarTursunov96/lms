import nested_admin
from django.contrib import admin
from .models import Article, Qualification, CourseSection, CourseBulletPoint, Blogs, Tutor, Course, Review, Lecture,PageType, BlogType
from quiz.models import Quiz, Question, Choice,CourseItem

# Register CourseSection and Lecture explicitly
@admin.register(CourseSection)
class CourseSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
    search_fields = ('title', 'course__title')
    list_filter = ('course__title', 'order')
    exclude = ('order',)

@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('id', 'section', 'title', 'video_url', 'duration')
    search_fields = ('id', 'section', 'title', 'video_url')
    list_filter = ('section__course__title', 'section__title')

# Register Course with nested inlines
class ChoicesInline(nested_admin.NestedStackedInline):
    model = Choice
    extra = 1

class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    extra = 1
    inlines = [ChoicesInline]

class LectureInline(nested_admin.NestedStackedInline):
    model = Lecture
    extra = 1
    fields = ('id', 'title', 'video_url', 'duration')
    readonly_fields = ('id',)
# class LectureInline(nested_admin.NestedTabularInline):
#     model = Lecture
#     extra = 1

# class CourseItemInline(nested_admin.NestedStackedInline):
#     model = CourseItem
#     extra = 1

class ReviewInline(nested_admin.NestedStackedInline):
    model = Review
    extra = 1





class QuizInline(nested_admin.NestedStackedInline):
    model = Quiz
    extra = 1
    inlines = [QuestionInline]
    exclude = ('order',)

class CourseSectionInline(nested_admin.NestedStackedInline):
    model = CourseSection
    extra = 1
    inlines = [LectureInline,QuizInline]
    exclude = ('order',)

@admin.register(Course)
class CourseAdmin(nested_admin.NestedModelAdmin):
    list_display = ('title', 'course_type', 'tutor', 'rating', 'student_count', 'price')
    search_fields = ('title', 'tags', 'course_type')
    list_filter = ('course_type', 'tutor')
    inlines = [CourseSectionInline,ReviewInline]

# Other model registrations
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'organiser_full_name', 'organiser_email', 'created_at')
    search_fields = ('title', 'description', 'category', 'topic', 'organiser_full_name', 'organiser_email', 'organiser_phone')
    list_filter = ('created_at', 'category')

@admin.register(Blogs)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'page_type', 'blog_type', 'vimeo_url')
    search_fields = ('title', 'page_type', 'blog_type', 'vimeo_url', 'description')
    list_filter = ('page_type', 'blog_type')

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', )
    list_filter = ('name',)

@admin.register(PageType)
class PageTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', )
    list_filter = ('name',)



@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'institution')
    search_fields = ('title', 'institution')
    list_filter = ('institution',)

class QualificationInline(nested_admin.NestedStackedInline):
    model = Qualification
    extra = 1

class CourseInline(nested_admin.NestedStackedInline):
    model = Course
    extra = 1

@admin.register(Tutor)
class TutorAdmin(nested_admin.NestedModelAdmin):
    list_display = ('name', 'subject', 'experience_years', 'hourly_rate')
    search_fields = ('name', 'subject', 'description', 'experience_years')
    inlines = [QualificationInline,CourseInline]



admin.site.register(CourseBulletPoint)
