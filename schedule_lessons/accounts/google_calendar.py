'''This module creates a database in the admin page called 'google-calendar'.'''
from social_core.backends.google import GoogleOAuth2

class GoogleCalendar(GoogleOAuth2):
    '''This class sets the database name to google-calendar'''
    name = 'google-calendar'
