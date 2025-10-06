from django.db import models
from django.utils.translation import gettext_lazy as _
from account.models import User
from lms.models import Course, CourseSection
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.

class CourseItem(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='courseitems',
        verbose_name=_("Course"),
        blank=True,
        null=True
    )
    section = models.ForeignKey(
        CourseSection,
        on_delete=models.CASCADE,
        verbose_name=_("Section"),
        blank=True,
        null=True
    )
    order = models.PositiveIntegerField(_("Order"), blank=True, null=True)

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name=_("Content Type")
    )
    object_id = models.PositiveIntegerField(_("Object ID"), null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = _("Course Item")
        verbose_name_plural = _("Course Items")
        ordering = ["order"]

    def save(self, *args, **kwargs):
        if self.order is None:
            last_order = (
                CourseItem.objects.filter(section=self.section)
                .aggregate(models.Max("order"))["order__max"]
            )
            self.order = 1 if last_order is None else last_order + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.content_type.model} - Order: {self.order}"




class Quiz(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='quizzes_for_course',
        verbose_name=_("Course")
    )
    course_section = models.ForeignKey(
        CourseSection,
        on_delete=models.CASCADE,
        related_name='quizzes',
        verbose_name=_("Course Section"),
        blank=True,
        null=True
    )
    title = models.CharField(_("Title"), max_length=255)
    order = models.PositiveIntegerField(_("Order"), blank=True, null=True, default=None)
    description = models.TextField(_("Description"), blank=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)


    class Meta:
        verbose_name = _("Quiz")
        verbose_name_plural = _("Quizzes")
        ordering = ["order"]

    def save(self, *args, **kwargs):
        if self.order is None:
            last_order = Quiz.objects.filter(course=self.course).aggregate(models.Max("order"))["order__max"]
            self.order = 1 if last_order is None else last_order + 1
        super().save(*args, **kwargs)

    def total_questions(self):
        return self.questions.count()

    def __str__(self):
        return self.title



class Question(models.Model):
    QUESTION_TYPES = [
        ('MCQ', _("Multiple Choice")),
        ('TF', _("True/False")),
        ('Radio', _("Radio")),
    ]

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name=_("Quiz")
    )
    text = models.CharField(_("Question Text"), max_length=500)
    question_type = models.CharField(
        _("Question Type"),
        max_length=50,
        choices=QUESTION_TYPES,
        default='MCQ',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(_("Created At"), null=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices',
        verbose_name=_("Question")
    )
    text = models.CharField(_("Choice Text"), max_length=255)
    is_correct = models.BooleanField(_("Is Correct"), default=False)

    class Meta:
        verbose_name = _("Choice")
        verbose_name_plural = _("Choices")

    def __str__(self):
        return self.text

class QuizAttempt(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("User")
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        verbose_name=_("Quiz")
    )
    score = models.FloatField(_("Score"))
    completed_test = models.BooleanField(_("Completed Test"), default=False)
    started_at = models.DateTimeField(_("Started At"), auto_now_add=True)
    finished_at = models.DateTimeField(_("Finished At"), null=True, blank=True)

    class Meta:
        verbose_name = _("Quiz Attempt")
        verbose_name_plural = _("Quiz Attempts")

    def __str__(self):
        return f"{self.user.username}'s attempt on {self.quiz.title}"

class UserAnswer(models.Model):
    attempt = models.ForeignKey(
        QuizAttempt,
        related_name='user_answers',
        on_delete=models.CASCADE,
        verbose_name=_("Quiz Attempt")
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name=_("Question")
    )
    chosen_option = models.ForeignKey(
        Choice,
        on_delete=models.CASCADE,
        verbose_name=_("Chosen Option")
    )
    created_at = models.DateTimeField(_("Created At"), null=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("User Answer")
        verbose_name_plural = _("User Answers")
        ordering = ['-created_at']

class QuizProgress(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("User")
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        verbose_name=_("Quiz")
    )
    answered_questions = models.JSONField(_("Answered Questions"), default=list)
    current_question_index = models.IntegerField(_("Current Question Index"), default=0)
    last_updated = models.DateTimeField(_("Last Updated"), auto_now=True)

    class Meta:
        verbose_name = _("Quiz Progress")
        verbose_name_plural = _("Quiz Progresses")
        unique_together = ('user', 'quiz')

    def __str__(self):
        return f"{self.user.username}'s progress on {self.quiz.title}"