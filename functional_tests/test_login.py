from django.core import mail
from selenium.webdriver.common.keys import Keys
import re

from .base import FunctionalTest

TEST_EMAIL = 'simonbeyer79@gmail.com'
SUBJECT = 'Your login link for Superlists'

class LoginTest(FunctionalTest):

    def test_can_get_email_links_to_login(self):
        # Simon goes to the awesome superlists site
        # and notices a "Log in" section in the navbar for the first time
        # it'S telling him to enter his email-address, so he does
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # A message appears telling him an email has been sent
        self.wait_for(lambda: self.assertIn(
            'Check your mail',
            self.bro_wser.find_element_by_tag_name('body').text
        ))

        # he checks his mail and finds a message
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # it has a url link in it
        self.assertIn('Use this link to log in', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not  url_search:
            self.fail(f'Could not find url in email body:\n{email.body}')
        url=url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # he clicks it
        self.browser.get(url)

        # he is logged in
        self.wait_for(lambda:self.browser.find_element_by_link_text('Log out'))
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(TEST_EMAIL, navbar.text)


