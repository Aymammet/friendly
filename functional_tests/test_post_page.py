# from selenium import webdriver
# from django.test import TestCase, Client, LiveServerTestCase
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from django.urls import reverse 
# from profiles.models import User
# from post.models import Post
# import time

# class TestPostListPage(StaticLiveServerTestCase):
  
#     def setUp(self):
#         self.browser = webdriver.Chrome('functional_tests/chromedriver')
#         self.user = User.objects.create(username='user', email='user@gmail.com' ,password='userpassword')
#         self.client = Client()
#         self.client.force_login(self.user)

#     def tearDown(self):
#         self.browser.close()

#     def test_initial(self):
#         self.browser.get(self.live_server_url)
#         time.sleep(1)
#         # Login page displayed:
#         alert = self.browser.find_element_by_class_name('title')
#         self.assertEquals(alert.text, 'Login')


#     def test_register_page(self):
#         self.browser.get(self.live_server_url)
#         time.sleep(1)
        
#         #Redirected to register page:
#         add_url = self.live_server_url + reverse('authenticate:register')
#         self.browser.find_element_by_id('register-page').click()
#         self.assertEquals(self.browser.current_url, add_url)
    

#     def test_user_redirected_to_home_page(self):
#         self.browser.get(self.live_server_url)
#         # self.user = User.objects.create(username='user', email='user@gmail.com' ,password='userpassword')
#         # self.client = Client()
#         self.client.force_login(self.user)
#         time.sleep(10)
       