from django import template

register = template.Library()


@register.filter(name='format_user')
def format_user(value, user):
    if value.username == user.username:
        return 'You'
    else:
        return value.get_fullname
