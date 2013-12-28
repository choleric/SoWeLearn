from django.views.decorators.csrf import ensure_csrf_cookie

from allauth.socialaccount.views import LoginErrorView

from ... import settings
from ..response import JsonResponse
from .. import code

class LoginErrorViewLearn(LoginErrorView):
    def get(self, request):
        return JsonResponse(code.SocialAccountLoginFailed)

login_error_learn = LoginErrorViewLearn.as_view()