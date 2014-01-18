import json

from django.core.urlresolvers import reverse
from django.test import Client
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest

from ..projtest import BaseTest
from mylearn.apps import errcode
from middleware import ProcessAjaxRedirectMiddleware

class CSRFFetchTestCase(BaseTest):
    def test_csrf(self) :
        csrfURL = reverse("csrf_fetch")
        res = self.client.get(csrfURL)
        self.assertEquals(200, res.status_code, "status code %d" % (res.status_code))
        self.assertTrue("_t" in res.cookies and 1 == len(res.cookies), "csrf cookie %s" % (res.cookies))
        self.assertTrue(0 < len(res.cookies["_t"]), "csrf cookie %s" % (res.cookies["_t"]))

    def test_csrf_post_fail(self) :
        csrfURL = reverse("csrf_fetch")
        self.client = Client(enforce_csrf_checks=True)
        res = self.client.post(csrfURL)
        self.assertEquals(403, res.status_code, "status code %d" % (res.status_code))

    def test_csrf_manually_fetch(self) :
        csrfURL = reverse("csrf_fetch")
        self.client = Client(enforce_csrf_checks=True)
        res = self.client.get(csrfURL)
        self.assertEquals(200, res.status_code, "status code %d" % (res.status_code))

        token = res.cookies[settings.CSRF_COOKIE_NAME].value
        # check res
        self.client.defaults.update({"HTTP_X_CSRFTOKEN": token})
        res = self.client.post(csrfURL)
        self.assertEquals(200, res.status_code, "status code %d" % (res.status_code))
        self.assertTrue("_t" in res.cookies and 1 == len(res.cookies), "csrf cookie %s" % (res.cookies))
        self.assertTrue(0 < len(res.cookies["_t"]), "csrf cookie %s" % (res.cookies["_t"]))

class MiddlewareTestCase(BaseTest):

    def test_ajax_redirect_general(self):
        url = '/'
        request = HttpRequest()
        request.META['HTTP_X_REQUESTED_WITH']='XMLHttpRequest'
        response = HttpResponseRedirect(url)
        ProcessedResponse = ProcessAjaxRedirectMiddleware().process_response(request,response)

        self.assertEqual(ProcessedResponse.status_code, 200, response)
        content = json.loads(ProcessedResponse.content)
        self.assertEqual(content["c"], errcode.SUCCESS, content)
        self.assertEqual(content["d"], url)

    def test_non_ajax_redirect(self):
        url = '/'
        request = HttpRequest()
        response = HttpResponseRedirect(url)
        ProcessedResponse = ProcessAjaxRedirectMiddleware().process_response(request,response)

        self.assertEqual(ProcessedResponse.status_code, 302, response)
        self.assertEqual(ProcessedResponse['location'], url)

    def test_ajax_non_redirect(self):
        url = '/'
        request = HttpRequest()
        request.META['HTTP_X_REQUESTED_WITH']='XMLHttpRequest'
        response = HttpResponse("This is not a redirect response")
        response.status_code = 111
        ProcessedResponse = ProcessAjaxRedirectMiddleware().process_response(request,response)

        self.assertEqual(ProcessedResponse.status_code, 111, response)

    def test_ajax_redirect_signup(self):
        data ={'email': "signup@signup.com",'password1':"signup",'password2':"signup",
               'userFirstName':"ming", 'userLastName':'xing'}
        response = self.client.post(reverse('account_signup_learn'),
                                    data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200, response)
        content = json.loads(response.content)
        self.assertEqual(content["c"], errcode.SUCCESS, content)
        self.assertEqual(content["d"], reverse("account_email_verification_sent"))