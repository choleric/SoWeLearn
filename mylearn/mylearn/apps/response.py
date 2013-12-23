"""
This file contains base responses.
"""
import json 

from json import encoder
from django.http import HttpResponse
from django.utils import html

def __html_encode(o) :
    return __html_encode.originFunc(html.escape(o))

def html_entity_encode(o) :
    # replace default encode string function in encoder
    __html_encode.originFunc = encoder.encode_basestring_ascii
    encoder.encode_basestring_ascii = __html_encode

    content = json.dumps(o)

    # recover original encode string function
    encoder.encode_basestring_ascii = __html_encode.originFunc 
    return content

"""
Automatically setup json reponse.
Usage:
    return JsonResponse(code, data)
"""
class JsonResponse(HttpResponse) :

    def __init__(self, code = None, data = None, status = 200, isHTMLEncode = True) :
        if None == code :
            raise Exception("JsonResponse needs a code")
        responseData = {"c": int(code)}
        if None != data :
            responseData["d"] = data

        content = None
        if isHTMLEncode :
            content = html_entity_encode(responseData)
        else :
            content = json.dumps(responseData)

        super(JsonResponse, self).__init__(
                content,
                "application/json",
                status)

