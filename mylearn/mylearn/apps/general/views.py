from django.http import HttpResponse

def csrf_token_fetch(request):
    request.META["CSRF_COOKIE_USED"] = True
    return HttpResponse("")
