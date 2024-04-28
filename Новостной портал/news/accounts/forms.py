from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        just_users = Group.objects.get(name="just users")
        user.groups.add(just_users)
        return user