from unittest import skip

from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest
from lists.forms import DUPLICATE_ITEM_ERROR


class ItemValidationTest(FunctionalTest):
    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_list_items(self):
        # Edith goes to the homepage and accidently tries to submit
        # an empty list item. She hits Enter on the Empty input box
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # the browser intercepts the request and does not load the
        # list page
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector(
                '#id_text:invalid'
            )
        )

        # she starts typing some text for the new item and the error disappears
        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector(
                '#id_text:valid'
            )
        )

        # and she can submit it successfully
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # perversely she now decides to submit a second blank list item
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Again the browser will not comply
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector(
                '#id_text:invalid'
            )
        )

        # And she can correct it by filling some text in
        self.get_item_input_box().send_keys('Make tea')
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector(
                '#id_text:valid'
            )
        )
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        # Edith goes to the homepage and starts a list
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy wellies')

        # she accidently tries to enter a duplicate item
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # she sees a helpful error message
        self.wait_for(
            lambda: self.assertEqual(
                self.get_error_element().text,
                DUPLICATE_ITEM_ERROR
            )
        )

    def test_error_messages_are_cleared_on_input(self):
        # Edith starts a list and causes a validation error
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Banter too thick')
        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(
            lambda: self.assertTrue(
                self.get_error_element().is_displayed()
            )
        )

        #she's starting in the input box to clear the error
        self.get_item_input_box().send_keys('a')

        # she is pleased to see that the error message disapears
        self.wait_for(
            lambda: self.assertFalse(
                self.get_error_element().is_displayed()
            )
        )
