import unittest

from django.test import LiveServerTestCase
from selenium import webdriver


class NewVisitorTest(LiveServerTestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)


if __name__ == '__main__':
    unittest.main(warnings='ignore')

# import unittest
#
# from selenium import webdriver
#
# class NewVisitorTest(unittest.TestCase):
#     def setUp(self) -> None:
#         self.browser = webdriver.Firefox()
#         self.browser.implicitly_wait(3)
#
#     def tearDown(self) -> None:
#         self.browser.quit()
#
#     def test_can_start_a_list_and_retrieve_it_later(self):
#         self.browser.get('http://localhost:8000')
#         self.assertIn('SpartaGYM', self.browser.title)
#         header_text = self.browser.find_element_by_tag_name('h2').text
#         self.assertIn('СПАРТА -\nСПОРТ ВЫСШЕЙ КАТЕГОРИИ!', header_text)
#         # self.fail("Finish the test!")
#
#
# if __name__ == '__main__':
#     unittest.main(warnings='ignore')
