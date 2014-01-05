from django.core.urlresolvers import reverse
from ..projtest import BaseTest

class CSRFFetchTestCase(BaseTest):
    def test_csrf(self) :
        csrfURL = reverse("csrf_fetch")
        res = self.client.get(csrfURL)
        self.assertEquals(200, res.status_code, "status code %d" % (res.status_code))
        self.assertTrue("_t" in res.cookies and 1 == len(res.cookies), "csrf cookie %s" % (res.cookies))
        self.assertTrue(0 < len(res.cookies["_t"]), "csrf cookie %s" % (res.cookies["_t"]))

