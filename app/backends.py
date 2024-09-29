from django.contrib.auth.backends import ModelBackend
from cqt_app.models import User  # Adjust the import based on your project structure

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)  # username is actually the email here
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
