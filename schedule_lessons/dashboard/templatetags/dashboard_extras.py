'''This module creates new template tagging used for creating variables.'''
from django.template import Library
register = Library()
SOME_VARIABLE = "first_text"
@register.simple_tag
def define_variable(variable):
    '''Defines a global variable for template tagging.'''
    global SOME_VARIABLE
    SOME_VARIABLE = variable
    return ''

@register.simple_tag
def get_variable():
    '''Used to get a global variable.'''
    global SOME_VARIABLE
    return SOME_VARIABLE
