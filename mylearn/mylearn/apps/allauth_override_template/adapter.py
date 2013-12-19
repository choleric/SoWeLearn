from allauth.account.adapter import DefaultAccountAdapter
from ..response import JsonResponse
from .. import code

class AccountAdapter(DefaultAccountAdapter):
    def ajax_response(self, request, response, redirect_to=None, form=None):
        data = {}
        if redirect_to:
            status = 200
            data['location'] = redirect_to
        if form:
            if form.is_valid():
                status = 200
            else:
                status = 400
                data['form_errors'] = form._errors
            if hasattr(response, 'render'):
                response.render()
            data['html'] = response.content.decode('utf8')
        return JsonResponse(code.SignupFailure, data)
