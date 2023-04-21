import pymongo
import requests
from django.test import Client
from django.test import TestCase
import sys
import os

def assertEqual( a, b):
    if a != b:
        raise Exception(f"{a} != {b}")
    else:
        print("Response: PASS")

def assertRedirects( response, url):
    if response.url != url:
        raise Exception(f"{response.url} != {url}")
    else:
        print("Redirects: PASS")

def assertTemplateUsed( response, template):
    if template not in response.templates[0].name:
        raise Exception(f"{template} not in {response.templates[0].name}")
    else:
        print("Template: PASS")


class LoginTestCase(TestCase):
    def __init__(self):
        self.c = Client()
        print("Login Test Case Started ---------------------------------------------")
        

    def setUp(self):
        # Connect to MongoDB
        client = pymongo.MongoClient("mongodb+srv://superuser:superuser%40SWE30@swe-cluster.xxvswrz.mongodb.net/?retryWrites=true&w=majority")
        db = client['swe_test_db']
        self.collection = db['users']
        new_user = {
            'UserName': 'testuser',
            'Password': 'testpass',
            'ConfirmPassword': 'testpass',
            'Email': 'test@gmail.com',
            'FirstName': 'test',
            'LastName': 'user',
            'DOB': '2002-07-20'
        }
        # Create a test user
        # user = User.objects.create_user(UserName='testuser', password='testpass')
        self.collection.insert_one(new_user)
        
    def test_login(self):
        response = self.c.post('/myApp/login/', {'UserName': 'testuser', 'Password': 'testpass'})
        assertEqual(response.status_code, 302) # redirect to home
        assertRedirects(response, '/myApp')
        print("Login: PASS")
        
    def test_login_failure(self):
        response = self.c.post('/myApp/login/', {'UserName': 'testuser', 'Password': 'wrongpass'})
        assertEqual(response.status_code, 200) # stay in login page
        assertTemplateUsed(response, 'myApp/login.html')
        print("Login Failure: PASS")

    def tearDown(self):
        client = pymongo.MongoClient("mongodb+srv://superuser:superuser%40SWE30@swe-cluster.xxvswrz.mongodb.net/?retryWrites=true&w=majority")
        db = client['swe_test_db']
        self.collection = db['users']
        self.collection.delete_many({'UserName': 'testuser'})
        print("Login Test Case Ended ---------------------------------------------")

    def runTest(self):
        self.setUp()
        self.test_login()
        self.test_login_failure()
        self.tearDown()

test = LoginTestCase()
test.runTest()
class RegisterTestCase(TestCase):
    def _init_(self):
        self.c = Client()
        print("Register Test Case Started ---------------------------------------------")

    def Register(self):
        new_user = {
            'UserName': 'testuser',
            'Password': 'testpass',
            'ConfirmPassword': 'testpass',
            'Email': 'test@gmail.com',
            'FirstName': 'test',
            'LastName': 'user',
            'DOB': '2002-07-20'
        }
        response = self.c.post('/myApp/register/', new_user)
        assertEqual(response.status_code, 302)
        assertRedirects(response, '/myApp')
        print("Register: PASS")

    def signOut(self):
        response = self.c.get('/myApp/logout/')
        assertEqual(response.status_code, 302)
        assertRedirects(response, '/myApp')
        print("Sign Out: PASS")
    
    def Login(self):
        response = self.c.post('/myApp/login/', {'UserName': 'testuser', 'Password': 'testpass'})
        assertEqual(response.status_code, 302)
        assertRedirects(response, '/myApp')
        print("Login: PASS")
    
    def tearDown(self):
        client = pymongo.MongoClient("mongodb+srv://superuser:superuser%40SWE30@swe-cluster.xxvswrz.mongodb.net/?retryWrites=true&w=majority")
        db = client['swe_test_db']
        self.collection = db['users']
        self.collection.delete_many({'UserName': 'testuser'})
        print("Register Test Case Ended ---------------------------------------------")


    def runTest(self):
        self.Register()
        self.signOut()
        self.Login()
        self.tearDown()

test = RegisterTestCase()
test.runTest()

class DuplicateRegisterTestCase(TestCase):
    def _init_(self):
        self.c = Client()
        print("Duplicate Register Test Case Started ---------------------------------------------")
    def setUp(self):
        # Connect to MongoDB
        client = pymongo.MongoClient("mongodb+srv://superuser:superuser%40SWE30@swe-cluster.xxvswrz.mongodb.net/?retryWrites=true&w=majority")
        db = client['swe_test_db']
        self.collection = db['users']
        new_user = {
            'UserName': 'testuser',
            'Password': 'testpass',
            'ConfirmPassword': 'testpass',
            'Email': 'test@gmail.com',
            'FirstName': 'test',
            'LastName': 'user',
            'DOB': '2002-07-20'
        }
        # Create a test user
        # user = User.objects.create_user(UserName='testuser', password='testpass')
        self.collection.insert_one(new_user)
    def Register(self):
        new_user = {
            'UserName': 'testuser',
            'Password': 'testpass',
            'ConfirmPassword': 'testpass',
            'Email': 'test@gmail.com',
            'FirstName': 'test',
            'LastName': 'user',
            'DOB': '2002-07-20'
        }
        response = self.c.post('/myApp/register/', new_user)
        assertEqual(response.status_code, 200) # stay in login page
        assertTemplateUsed(response, 'myApp/register.html')
        print("Duplicate Register: PASS")
    def tearDown(self):
        client = pymongo.MongoClient("mongodb+srv://superuser:superuser%40SWE30@swe-cluster.xxvswrz.mongodb.net/?retryWrites=true&w=majority")
        db = client['swe_test_db']
        self.collection = db['users']
        self.collection.delete_many({'UserName': 'testuser'})
        print("Duplicate Register Test Case Ended ---------------------------------------------")
    def runTest(self):
        self.setUp()
        self.Register()
        self.tearDown()

test = DuplicateRegisterTestCase()
test.runTest()