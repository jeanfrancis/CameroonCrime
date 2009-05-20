from django.core import mail
from django.test import TestCase

from models import Moniton


class MonitonTestCase(TestCase):
    """
    Test operations for crime areas monitoring.
    """
    urls = 'monitor.urls'
    fixtures = ['monitor/fixtures/monitons.json']

    def setUp(self):
        pass

    def test_get_subscribe(self):
        """
        Test accessing subscribe page.
        """
        response = self.client.get('/subscribe/')
        self.assertTemplateUsed(response, 'monitor/subscribe.html')

    def test_post_subscribe(self):
        """
        Test subscribing to monitor.
        """
        inputs = {
            'email': 'kegan@kegan.info',
            'north': 1.1234,
            'east': 1.1234,
            'south': 1.1234,
            'west': 1.1234,
        }
        response = self.client.post('/subscribe/', inputs)

        self.assertEquals(mail.outbox[0].to, [inputs['email']])
        self.assertEquals(mail.outbox[0].subject, 'Confirmation of Malaysia Crime Monitor subscription')
        self.assertRedirects(response, 'subscribe/done/?uuid=%s' % Moniton.objects.latest('created_at').add_uuid)

    def test_post_subscribe_email_invalid(self):
        """
        Test subscribing to monitor.
        """
        inputs = {
            'email': 'xxx',
            'north': 1.1234,
            'east': 1.1234,
            'south': 1.1234,
            'west': 1.1234,
        }
        response = self.client.post('/subscribe/', inputs, follow=True)
        self.assertFormError(response, 'form', 'email', 'Enter a valid e-mail address.')

    def test_get_subscribe_confirm(self):
        """
        Test confirmation a subscription.
        """
        response = self.client.get('/subscribe/confirm/', {'uuid': '03619ac2453211de8c651fabc0151a16'})
        self.assertTemplateUsed(response, 'monitor/subscribe_confirm.html')

        self.assertEquals(response.context['email'], 'unconfirm@example.com')
        self.assertTrue(Moniton.objects.get(email='unconfirm@example.com').registered)

    def test_get_subscribe_confirm_uuid_invalid(self):
        """
        Test confirmation a subscription.
        """
        response = self.client.get('/subscribe/confirm/', {'uuid': 'xxx'})
        self.assertTemplateUsed(response, '404.html')

    def test_get_unsubscribe_done(self):
        """
        Test requesting email for unsubscription confirmation.
        """
        response = self.client.get('/unsubscribe/done/', {'uuid': '45368b7c454311de829b33b9aa2110db'})
        self.assertTemplateUsed(response, 'monitor/unsubscribe_done.html')

        self.assertEquals(mail.outbox[0].to, ['confirm@example.com'])
        self.assertEquals(mail.outbox[0].subject, 'Confirmation of Malaysia Crime Monitor unsubscription')

    def test_get_unsubscribe_done_uuid_invalid(self):
        """
        Test requesting email for unsubscription confirmation with invalid uuid.
        """
        response = self.client.get('/unsubscribe/done/', {'uuid': 'xxx'})
        self.assertTemplateUsed(response, '404.html')

    def test_get_unsubscribe_confirm(self):
        """
        Test confirmation an unsubscription.
        """
        response = self.client.get('/unsubscribe/confirm/', {'uuid': '4ad2302c454311de8b3387c74347e6f7'})
        self.assertTemplateUsed(response, 'monitor/unsubscribe_confirm.html')
        self.assertFalse(Moniton.objects.filter(email='confirm@example.com'))

    def test_get_unsubscribe_confirm_uuid_invalid(self):
        """
        Test confirmation an unsubscription with invalid uuid.
        """
        response = self.client.get('/unsubscribe/confirm/', {'uuid': 'xxx'})
        self.assertTemplateUsed(response, '404.html')

    def tearDown(self):
        pass


# Disabled TEMPLATE_DIRS so that custom templates would not intefere with tests.
from django.conf import settings
settings.TEMPLATE_DIRS = ()
