from datetime import datetime


class LoginForm():
    def __init__(self, data):
        self.UserName = data['UserName']
        self.Password = data['Password']
    def is_valid(self):
        return True

class RegisterationForm():
    def __init__(self, data):
        self.UserName = data['UserName']
        self.FirstName = data['FirstName']
        self.LastName = data['LastName']
        self.Email = data['Email']
        self.Password = data['Password']
    def is_valid(self):
        return True
    
class PostForm():
    def __init__(self, data, username):
        self.title = data['Title']
        self.description = data['Description']
        self.author = username
        self.post_ID = username + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    def is_valid(self):
        return True