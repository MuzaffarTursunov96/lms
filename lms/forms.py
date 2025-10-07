from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Course
from modeltranslation.utils import get_translation_fields

class CourseAdminForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add CKEditor to base fields and all translated fields
        richtext_fields = ["overview", "syllabus", "outcomes", "teachers"]
        for field_name in richtext_fields:
            for lang_field in get_translation_fields(field_name):
                if lang_field in self.fields:
                    self.fields[lang_field].widget = CKEditor5Widget(config_name="extends")
