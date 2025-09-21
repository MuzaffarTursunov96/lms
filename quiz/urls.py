from django.urls import path
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import views2


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'quizzes', views.QuizViewSet, basename='quiz')
router.register(r'questions', views.QuestionViewSet, basename='question')
router.register(r'quiz-attempts', views.QuizAttemptViewSet, basename='quiz-attempt')
router.register(r'user-answers', views.UserAnswerViewSet, basename='user-answer')




urlpatterns = [
    
    path('quiz/<int:id>', views.quiz_entry, name='quiz'),
    path('quiz-results/<int:id>', views.quiz_results, name='quiz_results'),
    path('quiz/<int:id>/retake/', views.retake_quiz, name='retake_quiz'),

    #### Quiz ####
    path('api/quiz/<int:id>/questions/', views.get_quiz_data, name='get_quiz_data'),
    path('api/quiz/<int:id>/submit/', views.submit_quiz, name='submit_quiz'),

    # path('api/v1/', include(router.urls)),

    # API endpoint to get a quiz and its remaining questions
    path('api/v1/q/<int:id>/progress/', views2.get_quiz_with_progress, name='quiz_progress'),
    path('api/v1/q/<int:id>/start/', views2.start_new_attempt, name='quiz_start'),
    

]