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
        self.ConfirmPassword = data['ConfirmPassword']
        self.DOB = data['DOB']
    def is_valid(self):
        return True
    
class PostIncidentForm():
    def __init__(self, data, username):
        self.title = data['Title']
        self.description = data['Description']
        self.longitude = data['Longitude']
        self.latitude = data['Latitude']
        self.author = username
        self.incident_type = 0
        self.time = data['Time']
        self.is_authentic = False
        self.upvotes = 0
        self.downvotes = 0
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
        self.score = 0
        self.pincode = data['Pincode']
        self.city = data['City']
        self.state = data['State']
        self.country = data['Country']
        self.address_line1 = data['AddressLine1']
        self.address_line2 = data['AddressLine2']
        self.post_ID = username + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    def is_valid(self):
        return True
    
class ChangePasswordForm():
    def __init__(self, data):
        self.UserName = data['UserName']
        self.DOB = data['DOB']
        self.new_password = data['newPassword']
        self.confirm_password = data['confirmNewPassword']
    def is_valid(self):
        return (self.confirm_password==self.new_password)