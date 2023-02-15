from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            print(username, password)
            user = UserModel.objects.get(email=username)
            print(user)
        except UserModel.DoesNotExist:
            print("User doesnt exit")
            return None
        if user.check_password(password) and user.is_active:
            return user     
        return None
    
    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            print("User doesnt exit")
            return None
