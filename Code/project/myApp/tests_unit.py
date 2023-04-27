import pymongo
import requests
from django.test import Client
from django.test import TestCase
import sys
import os

class LoginTestCase(TestCase):
    @classmethod
    def setUpClass(self):
        super(LoginTestCase, self).setUpClass()
        self.client = pymongo.MongoClient("mongodb+srv://superuser:superuser%40SWE30@swe-cluster.xxvswrz.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client['swe_test_db']
        self.collection = self.db['users']
        new_user = {'UserName': 'testuser', 'Password': 'testpass', 'Email': 'test@gmail.com', 'FirstName': 'test', 'LastName': 'user', 'DOB': '2002-07-20'}
        self.collection.insert_one(new_user)

    @classmethod
    def tearDownClass(self):
        super(LoginTestCase, self).tearDownClass()
        self.collection.delete_many({'UserName': 'testuser'})

    # test login success
    def test_login(self):
        response = self.client.post('/myApp/login/', {'UserName': 'testuser', 'Password': 'testpass'})
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/myApp/')
        self.assertTemplateUsed(response, 'myApp/reg_hmpg.html')
        self.client.get('/myApp/logout/')
        
    # test login failure
    def test_login_failure(self):
        response = self.client.post('/myApp/login/', {'UserName': 'testuser', 'Password': 'wrongpass'})
        self.assertEqual(response.status_code, 200)

    # test no input
    def test_login_no_input(self):
        response = self.client.post('/myApp/login/', {'UserName': '', 'Password': ''})
        self.assertEqual(response.status_code, 200)

    # test only username input
    def test_login_only_username(self):
        response = self.client.post('/myApp/login/', {'UserName': 'testuser', 'Password': ''})
        self.assertEqual(response.status_code, 200)

    # test only password input
    def test_login_only_password(self):
        response = self.client.post('/myApp/login/', {'UserName': '', 'Password': 'testpass'})
        self.assertEqual(response.status_code, 200)

class RegisterTestCase(TestCase):
    @classmethod
    def setUpClass(self):
        super(RegisterTestCase, self).setUpClass()
        self.client = pymongo.MongoClient("mongodb+srv://superuser:superuser%40SWE30@swe-cluster.xxvswrz.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client['swe_test_db']
        self.collection = self.db['users']

    @classmethod
    def tearDownClass(self):
        super(RegisterTestCase, self).tearDownClass()
        self.collection.delete_many({'UserName': 'testuser'})

    # test register success
    def test_register(self):
        response = self.client.post('/myApp/register/', {'UserName': 'testuser', 'Password': 'testpass', 'ConfirmPassword': 'testpass', 'Email': 'test@gmail.com', 'FirstName': 'test', 'LastName': 'user', 'DOB': '2002-07-20'})
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/myApp/')
        self.assertTemplateUsed(response, 'myApp/reg_hmpg.html')
        self.client.get('/myApp/logout/')
        self.collection.delete_many({'UserName': 'testuser'})

    # test register failure due to same username
    def test_register_failure(self):
        response = self.client.post('/myApp/register/', {'UserName': 'testuser', 'Password': 'testpass', 'ConfirmPassword': 'testpass', 'Email': 'test@gmail.com', 'FirstName': 'test', 'LastName': 'user', 'DOB': '2002-07-20'})
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/myApp/')
        self.assertTemplateUsed(response, 'myApp/reg_hmpg.html')
        self.client.get('/myApp/logout/')
        response = self.client.post('/myApp/register/', {'UserName': 'testuser', 'Password': 'testpass', 'ConfirmPassword': 'testpass', 'Email': 'test@gmail.com', 'FirstName': 'test', 'LastName': 'user', 'DOB': '2002-07-20'})
        self.assertEqual(response.status_code, 200)
        self.collection.delete_many({'UserName': 'testuser'})

    # test no input
    def test_register_no_input(self):
        response = self.client.post('/myApp/register/', {'UserName': '', 'Password': '', 'ConfirmPassword': '', 'Email': '', 'FirstName': '', 'LastName': '', 'DOB': ''})
        self.assertEqual(response.status_code, 200)

    # test only username input
    def test_register_only_username(self):
        response = self.client.post('/myApp/register/', {'UserName': 'testuser', 'Password': '', 'ConfirmPassword': '', 'Email': '', 'FirstName': '', 'LastName': '', 'DOB': ''})
        self.assertEqual(response.status_code, 200)
        
    # test invalid email
    def test_register_invalid_email(self):
        response = self.client.post('/myApp/register/', {'UserName': 'testuser', 'Password': 'testpass', 'ConfirmPassword': 'testpass', 'Email': 'test', 'FirstName': 'test', 'LastName': 'user', 'DOB': '2002-07-20'})
        self.assertEqual(response.status_code, 200)

    # test password mismatch
    def test_register_password_mismatch(self):
        response = self.client.post('/myApp/register/', {'UserName': 'testuser', 'Password': 'testpass', 'ConfirmPassword': 'wrongpass', 'Email': 'test@gmail.com', 'FirstName': 'test', 'LastName': 'user', 'DOB': '2002-07-20'})
        self.assertEqual(response.status_code, 200)


# post incident test case
class PostIncidentTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(PostIncidentTestCase, cls).setUpClass()
        cls.client = pymongo.MongoClient("mongodb+srv://superuser:superuser%40SWE30@swe-cluster.xxvswrz.mongodb.net/?retryWrites=true&w=majority")
        cls.db = cls.client['swe_test_db']
        cls.collection = cls.db['users']
        cls.collection.insert_one({'UserName': 'testuser', 'Password': 'testpass', 'Email': 'test@gmail.com', 'FirstName': 'test', 'LastName': 'user', 'DOB': '2002-07-20'})
        cls.collection = cls.db['incident']

    @classmethod
    def tearDownClass(cls):
        super(PostIncidentTestCase, cls).tearDownClass()
        cls.collection = cls.db['users']
        cls.collection.delete_many({'UserName': 'testuser'})
        cls.collection = cls.db['incident']
        cls.collection.delete_many({'title': 'test'})

    # test post incident success after login assuming user is already registered
    def test_post_incident(self):
        response = self.client.post('/myApp/login/', {'UserName': 'testuser', 'Password': 'testpass'})
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/myApp/postIncident/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/myApp/postIncident/', {'Title': 'test', 'Description': 'test', 'Latitude': '0', 'Longitude': '0', 'Time': '2021-04-20T00:00','crime-or-hazard': 'crime','IncidentType': 'Cybercrime'})
        self.assertEqual(response.status_code, 302)
        self.client.get('/myApp/logout/')
        self.collection.delete_many({'title': 'test'})

    # test post incident failure because of not logged in
    def test_post_incident_failure(self):
        response = self.client.post('/myApp/postIncident/', {'Title': 'test', 'Description': 'test', 'Latitude': '0', 'Longitude': '0', 'Time': '2021-04-20T00:00','crime-or-hazard': 'crime','IncidentType': 'Cybercrime'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/myApp/login/')

    # test post incident failure because of invalid input
    def test_post_incident_invalid_input(self):
        response = self.client.post('/myApp/login/', {'UserName': 'testuser', 'Password': 'testpass'})
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/myApp/postIncident/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/myApp/postIncident/', {'Title': '', 'Description': '', 'Latitude': float(), 'Longitude': float(), 'Time': '','crime-or-hazard': '','IncidentType': ''})
        self.assertEqual(response.status_code, 200)
        self.client.get('/myApp/logout/')