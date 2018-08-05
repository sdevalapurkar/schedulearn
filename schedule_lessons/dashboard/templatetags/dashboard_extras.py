from django.template import Library
register = Library()
somevariable = "first_text"
@register.simple_tag
def define_variable(variable):
    global somevariable
    somevariable = variable
    return ''

@register.simple_tag
def get_variable():
    global somevariable
    return somevariable
