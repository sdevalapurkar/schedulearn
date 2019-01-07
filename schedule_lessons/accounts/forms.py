from allauth.account.forms import SignupForm
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

class MyCustomSignupForm(SignupForm):

    def save(self, request):
        full_name_list = request.POST.get('user_name').split()
        adapter = get_adapter(request)
        user = adapter.new_user(request)
        user.first_name = full_name_list[0]
        if len(full_name_list) > 1:
            user.last_name = full_name_list[1]
        user.save()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        # TODO: Move into adapter `save_user` ?
        setup_user_email(request, user, [])
        return user
