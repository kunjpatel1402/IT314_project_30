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
    
class PostIncidentForm():
    def __init__(self, data, username):
        self.title = data['Title']
        self.description = data['Description']
        self.longitude = data['Longitude']
        self.latitude = data['Latitude']
        self.author = username
        self.curtime = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.post_ID = username + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    def is_valid(self):
        return True
    
class PostPropertyForm():
    def __init__(self, data, username):
        self.title = data['Title']
        self.description = data['Description']
        self.longitude = data['Longitude']
        self.latitude = data['Latitude']
        self.author = username
        self.is_authentic = False
        self.upvotes = 0
        self.downvotes = 0
        self.score = 0
        self.post_ID = username + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    def is_valid(self):
        return True
