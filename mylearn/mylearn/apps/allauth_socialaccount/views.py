import logging
from allauth.account.utils import user_email
from allauth.socialaccount.models import SocialLogin
from allauth.utils import email_address_exists
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie

from allauth.socialaccount.views import LoginErrorView, LoginCancelledView, SignupView, ConnectionsView

from ... import settings
from ..response import JsonResponse
from .. import code

logger = logging.getLogger(__name__)

class LoginCancelledViewLearn(LoginCancelledView):
    def get(self, request):
        return JsonResponse(code.SocialAccountLoginCancelled)

login_cancelled_learn = LoginCancelledViewLearn.as_view()

class SignupViewLearn(SignupView):
    def dispatch(self, request, *args, **kwargs):
        self.sociallogin = SocialLogin \
            .deserialize(request.session.get('socialaccount_sociallogin'))
        if not self.sociallogin:
            return HttpResponseRedirect(reverse('account_login'))
        email = user_email(self.sociallogin.account.user)
        if email:
            if email_address_exists(email):
                status = email_address_exists(email)
                return JsonResponse(code.DuplicateEmailSocialAccount, reverse('account_signin_learn'))
        return super(SignupView, self).dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        data = dict(form.errors.items())
        return JsonResponse(code.SocialAccountSignupFailure)

signup_learn = SignupViewLearn.as_view()

class ConnectionsViewLearn(ConnectionsView):
    def form_invalid(self, form):
        data = dict(form.errors.items())
        errMsg = data.get('__all__', ['Unkown Error'])[0]
        logger.debug('connections: %s'% data)
        return JsonResponse(code.AllAuthErrorMessageMap.get(errMsg, code.SocialConnectionFailed))

social_connections = ConnectionsViewLearn.as_view()
