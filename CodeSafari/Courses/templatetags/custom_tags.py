from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    """Adds class to form fields"""
    if hasattr(value, 'as_widget'):  # Check if 'value' has 'as_widget' method
        return value.as_widget(attrs={'class': arg})
    return value  # Return unchanged if not a form field
