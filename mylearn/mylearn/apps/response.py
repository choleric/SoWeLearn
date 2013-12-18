"""
This file contains base responses.
"""

import json
from django.http import HttpResponse

"""
Automatically setup json reponse.
Usage:
    return JsonResponse(code, data)
"""
class JsonResponse(HttpResponse) :

    def __init__(self, code = None, data = None, status = 200) :
        if None == code :
            raise Exception("JsonResponse needs a code")
        responseData = {"c": int(code)}
        if None != data :
            responseData["d"] = data
        super(JsonResponse, self).__init__(
                json.dumps(responseData),
                "application/json",
                status)

