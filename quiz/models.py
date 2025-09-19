from django.db import models
from account.models import User
from lms.models import Course, CourseSection
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.

class CourseItem(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='courseitems', blank=True, null=True)
    section = models.ForeignKey(CourseSection, on_delete=models.CASCADE,blank=True,null=True)
    order = models.PositiveIntegerField()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = "Course item order"
        verbose_name_plural = "Course Item orders"
        ordering = ['order']  # Default order by 'order' field
    def __str__(self):
        return f"{self.content_type.model} - Order: {self.order}"




class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes_for_course')
    course_section = models.ForeignKey(CourseSection, on_delete=models.CASCADE,blank=True, null=True,related_name='quizzes')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_questions(self):
        return self.questions.count()

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=500)
    question_type = models.CharField(max_length=50, choices=[('MCQ', 'Multiple Choice'), ('TF', 'True/False'),('Radio','Radio')], default='MCQ',blank=True, null=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField()
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s attempt on {self.quiz.title}"

class UserAnswer(models.Model):
    attempt = models.ForeignKey(QuizAttempt, related_name='user_answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    chosen_option = models.ForeignKey(Choice, on_delete=models.CASCADE)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True)

class QuizProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    answered_questions = models.JSONField(default=list)
    current_question_index = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'quiz')

    def __str__(self):
        return f"{self.user.username}'s progress on {self.quiz.title}"