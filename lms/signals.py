from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import Lecture
from quiz.models import Quiz, CourseItem


def create_course_item(instance, section):
    content_type = ContentType.objects.get_for_model(instance.__class__)
    print(instance,section,content_type,'<<<<<')
    if not CourseItem.objects.filter(
        section=section,
        content_type=content_type,
        object_id=instance.id
    ).exists():
        CourseItem.objects.create(
            section=section,
            content_type=content_type,
            object_id=instance.id
        )


@receiver(post_save, sender=Lecture)
def auto_create_courseitem_for_lecture(sender, instance, created, **kwargs):
    print("📢 Signal fired for Lecture:", instance.title, "created:", created)
    if created:
        create_course_item(instance, instance.section)


@receiver(post_save, sender=Quiz)
def auto_create_courseitem_for_quiz(sender, instance, created, **kwargs):
    print("📢 Signal fired for Quiz:", instance, "created:", created)
    if created:
        # here quiz points directly to course, so decide section logic
        # If quiz is linked to a section, use instance.section instead
        # Otherwise you may need to pick a default section
        if created and instance.course_section:
            create_course_item(instance, instance.course_section)
