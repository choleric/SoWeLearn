from ..response import JsonResponse
from mylearn.apps import errcode

class ProcessAjaxRedirectMiddleware(object):

    def process_response(self, request, response):
        # first check if the request is Ajax request
        #if getattr(request,'X-Requested-With')=='XMLHttpRequest':
        if request.is_ajax():
            # then check if the response is redirect
            if response.status_code == 302 and "location" in response:
                return JsonResponse(errcode.SUCCESS, response["location"])
            else:
                return response
        else:
            return response





