from django import template

register = template.Library()

@register.filter
def get_correct_choice(choices):
    correct = choices.filter(is_correct=True).first()
    return correct.text if correct else ""
