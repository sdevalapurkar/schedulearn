from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

facebook_login = FacebookLogin.as_view()

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

google_login = GoogleLogin.as_view()
