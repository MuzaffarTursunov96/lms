from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class QuizConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'quiz'
    verbose_name = _("Quiz System")
    
