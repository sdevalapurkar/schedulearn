SECRET_KEY = '&tm9%utcwp=rzanx9%jxn27gnck^4#65316g&6fei94==dml*6'
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_HOST_USER = 'lesson_scheduler@schedulearn.com'
EMAIL_HOST_PASS = 'hackuvic2018'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '243916091300-hf2tirt56sqv8mfid7poipac9rpie57c.apps.googleusercontent.com'  #Paste CLient Key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'OlHJPD_zb3UvsDRLvlCUBpd-' #Paste Secret Key
AUTHENTICATION_BACKENDS = (
 'social_core.backends.open_id.OpenIdAuth',  # for Google authentication
 'social_core.backends.google.GoogleOpenId',  # for Google authentication
 'social_core.backends.google.GoogleOAuth2',  # for Google authentication
 'django.contrib.auth.backends.ModelBackend',
)
