from django.test import TestCase

from .models import *


today_date = datetime.date.today()


class ProductTypeModelTest(TestCase):
    def setUp(self) -> None:
        self.product_type = ProductType.objects.create(
            type_name="Sparta Gym's Gainer"
        )

    def test_saving_and_retrieving_products(self):
        self.assertEqual(self.product_type.type_name, "Sparta Gym's Gainer")
        self.assertEqual(self.product_type.id, 2)


class ProductModelTest(TestCase):
    def setUp(self) -> None:
        self.product_type = ProductType.objects.create(
            type_name="Sparta Gym's Gainer"
        )
        self.product = Product.objects.create(
            name='Gainer',
            product_type=self.product_type,
            price=100.00,
            weight=2.5,
            portions=25,
            description='Description',
            date=today_date
        )

    def test_product_model_data(self):
        self.assertEqual(self.product.name, 'Gainer')
        self.assertEqual(self.product.product_type, self.product_type)
        self.assertEqual(self.product.price, 100.00)
        self.assertEqual(self.product.weight, 2.5)
        self.assertEqual(self.product.portions, 25)
        self.assertEqual(self.product.description, 'Description')
        self.assertEqual(self.product.date, today_date)


class PostModelTest(TestCase):
    def setUp(self) -> None:
        self.post = Post.objects.create(
            title='Title',
            text='Text',
        )

    def test_post_model_data(self):
        self.assertEqual(self.post.title, 'Title')
        self.assertEqual(self.post.text, 'Text')


# from django.test import TestCase
# from django.urls import resolve
# from django.http import HttpRequest
# from django.template.loader import render_to_string
#
# from shop.views import home
# from users.views import signup_form
#
#
# class HomePageTest(TestCase):
#     def test_root_url_resolves_to_home_page_view(self):
#         found = resolve('/')
#         self.assertEqual(found.func, home)
#
#     def test_home_page_returns_correct_html(self):
#         request = HttpRequest()
#         response = home(request)
#         expected_html = render_to_string('shop/home.html')
#         self.assertEqual(response.content.decode(), expected_html)
#
#
# class RegisterPageTest(TestCase):
#     def test_root_url_resolves_to_register_page_view(self):
#         found = resolve('/users/signup/')
#         self.assertEqual(found.func, signup_form)


# import unittest
#
# from selenium import webdriver
#
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
#         # self.fail("Finish the test!")
#
#
# if __name__ == '__main__':
#     unittest.main(warnings='ignore')

# from selenium import webdriver
#
#
# browser = webdriver.Firefox()
# browser.get("http://localhost:8000")
#
# assert 'Document' in browser.title, "Browser title was " + browser.title
# browser.quit()
