'''This module configures the api package as a django app.'''
from django.apps import AppConfig


class ApiConfig(AppConfig):
    '''This class configures the name of the api app.'''
    name = 'api'
