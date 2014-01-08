from django.core.urlresolvers import reverse
from django.test import Client
from django.conf import settings
from ..projtest import BaseTest

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
