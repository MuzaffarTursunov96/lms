from modeltranslation.translator import register, TranslationOptions
from .models import Blogs,Tutor,Course,Review,CourseBulletPoint,CourseSection,Qualification,Article,Lecture
from quiz.models import Quiz, Question, Choice


@register(Article)
class PageTranslationOptions(TranslationOptions):
    fields = ('title','category','description','topic','helper_text1','helper_text2','helper_text3')


@register(Blogs)
class PageTranslationOptions(TranslationOptions):
    fields = ('title','description','helper_text1','helper_text2','helper_text3','helper_text4','helper_text5')


@register(Tutor)
class TutorTranslationOptions(TranslationOptions):
    fields = ('subject','description','helper_text1','helper_text2','helper_text3')


@register(Qualification)
class QualificationTranslationOptions(TranslationOptions):
    fields = ('title','institution')


@register(Course)
class CourseTranslationOptions(TranslationOptions):
    fields = ('title','subtitle','course_type','duration','weekly_study','course_type','payment_period','overview')


@register(CourseSection)
class CourseSectionTranslationOptions(TranslationOptions):
    fields = ('title','content')

@register(CourseBulletPoint)
class CourseBulletPointTranslationOptions(TranslationOptions):
    fields = ('text',)



@register(Review)
class ReviewTranslationOptions(TranslationOptions):
    fields = ('comment',)

@register(Quiz)
class QuizTranslationOptions(TranslationOptions):
    fields = ('title','description')

@register(Question)
class QuestionTranslationOptions(TranslationOptions):
    fields = ('text',)

@register(Choice)
class ChoiceTranslationOptions(TranslationOptions):
    fields = ('text',)
    
@register(Lecture)
class LectureTranslationOptions(TranslationOptions):
    fields = ('title',)

