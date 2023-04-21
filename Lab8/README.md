# Lab 8 Group 30
## Project Name:Crime and hazards measuring website
### Testing for registration and login functionality

### Functions Used by us for testing
```python
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

```
All of the assert functions check if both the arguments passed to them are equal, if yes, they will print pass, otherwise they will raise an exception that they are not equal.


### 1. User Login Functionality

#### Code:
``` python
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
```
After connecting to the database, a test user is created here with the parameters indicated in the code (username, password, email etc. ).
#### Test case 1: 
When the user enters the correct username and password (which is indicated by code 302), the user will be redirected to the home page. Hence the test case will be passed then.
#### Test case 2: 
When a user enters an incorrect username or password (which is indicated by code 200), the user will stay in the login page itself. 

At the end when the testing for login is over, the dummy data in the database will be deleted. This concludes unit testing for the login page.

![image](https://user-images.githubusercontent.com/75675477/233687980-f168141d-0dfe-4ce7-a57d-d70ef29d7b1c.png)


### 2. User Registeration Functionality

#### Code :
``` python
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
```
Once the database is connected to, a test user is generated with the specifications provided in the code, such as username, password, email, and so on.
#### Test case 1: 
When the user enters all the required information and submits it, a new user will be created and status code 302 will be returned indicating successful registration and the user will be redirected to the home page.
#### Test case 2: 
After the user has logged in, on clicking the signout button, the user will be logged out. This ensures that the logout functionality is working properly.
#### Test Case 3: 
After logout, when the same registered user enters the information he used while registration, the user is logged in successfully. This ensures that the registration functionality is working properly.

At the end when the testing for registration is over, the dummy data in the database will be deleted. This concludes unit testing for the registration page.

![image](https://user-images.githubusercontent.com/75675477/233688096-0040b9cb-3c6b-4226-8916-257d78188ce7.png)

### 3. Duplicate Registeration Testcase:
``` python
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
```
After connecting to the database and adding a dummy user, the testing is done for the duplicate registration as follows:
#### Test case 1: 
When another user with the exact same information already registered, is tried to be created, this results in failure of registration (as status code 200 is returned) and the user is kept on the registration page only. This ensures that the registration for one user is done only once.

At the end when the testing for registration is over, the dummy data in the database will be deleted. This concludes unit testing for the registration page.

![image](https://user-images.githubusercontent.com/75675477/233688165-05ef2646-0357-46c5-aad4-73db8c4668af.png)



