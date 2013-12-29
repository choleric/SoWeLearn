import logging
from django.views.decorators.csrf import ensure_csrf_cookie

<<<<<<< HEAD
from allauth.socialaccount.views import LoginErrorView, LoginCancelledView, SignupView
=======
from allauth.socialaccount.views import LoginErrorView,ConnectionsView
>>>>>>> 03c8a34259266cbdb96743954f493e934816e809

from ... import settings
from ..response import JsonResponse
from .. import code

logger = logging.getLogger(__name__)

class LoginErrorViewLearn(LoginErrorView):
    def get(self, request):
        return JsonResponse(code.SocialAccountLoginFailed)

login_error_learn = LoginErrorViewLearn.as_view()

<<<<<<< HEAD

class LoginCancelledViewLearn(LoginCancelledView):
    def get(self, request):
        return JsonResponse(code.SocialAccountLoginCancelled)

login_cancelled_learn = LoginCancelledViewLearn.as_view()

class SignupViewLearn(SignupView):
    def form_invalid(self, form):
        data = dict(form.errors.items())
        return JsonResponse(code.SocialAccountSignupFailure, data)

signup_learn = SignupViewLearn.as_view()
=======
class ConnectionsViewLearn(ConnectionsView):
    def form_invalid(self, form):
        data = dict(form.errors.items())
        errMsg = data.get('__all__', ['Unkown Error'])[0]
        logger.debug('connections: %s'% data)
        return JsonResponse(code.AllAuthErrorMessageMap.get(errMsg, code.SocialConnectionFailed))

social_connections = ConnectionsViewLearn.as_view()
>>>>>>> 03c8a34259266cbdb96743954f493e934816e809