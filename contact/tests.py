from django.test import SimpleTestCase

from .forms import ContactForm


class ContactFormSpamFilterTests(SimpleTestCase):
    def _form(self, **overrides):
        data = {
            'honeypot': '',
            'name': 'Max Mustermann',
            'email': 'max@example.com',
            'betreff': 'Yoga Anfrage',
            'nachricht': 'Hallo Julian, ich interessiere mich fuer eine Yogastunde und freue mich auf deine Rueckmeldung.',
        }
        data.update(overrides)
        return ContactForm(data=data)

    def test_accepts_normal_contact_request(self):
        form = self._form()

        self.assertTrue(form.is_valid())

    def test_rejects_filled_honeypot(self):
        form = self._form(honeypot='spam')

        self.assertFalse(form.is_valid())
        self.assertIn('honeypot', form.errors)

    def test_rejects_keyword_and_url_spam(self):
        form = self._form(
            betreff='SEO Angebot',
            nachricht='We can help you rank higher with SEO. Visit https://spam.example.com now.',
        )

        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)

    def test_rejects_multiple_links(self):
        form = self._form(
            nachricht='Hallo, bitte pruefe https://spam.example.com und www.spam-offer.com fuer Details.',
        )

        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
