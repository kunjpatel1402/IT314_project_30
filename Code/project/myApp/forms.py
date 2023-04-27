from datetime import datetime


class LoginForm():
    def __init__(self, data):
        self.UserName = data['UserName']
        self.Password = data['Password']
    def is_valid(self):
        if (self.UserName == '' or self.Password == ''): 
            return False
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
        self.UpVoted = {}
        self.DownVoted = {}
    def is_valid(self):
        if (self.Email.find('@') == -1 or self.Email.find('.') == -1):
            return False
        if (self.UserName == '' or self.FirstName == '' or self.LastName == '' or self.Email == '' or self.Password == '' or self.ConfirmPassword == '' or self.DOB == ''):
            return False
        if (self.Password != self.ConfirmPassword):
            return False
        return True
    def to_dict(self):
        return {
            'UserName': self.UserName,
            'FirstName': self.FirstName,
            'LastName': self.LastName,
            'Email': self.Email,
            'Password': self.Password,
            'DOB': self.DOB,
            'UpVoted': self.UpVoted,
            'DownVoted': self.DownVoted
        }
    
class EditDetailsForm():
    def __init__(self, data):
        self.FirstName = data['FirstName']
        self.LastName = data['LastName']
        self.Email = data['Email']
        self.DOB = data['DOB']
        self.AddressLine1 = data['AddressLine1']
        self.AddressLine2 = data['AddressLine2']
        self.Locality = data['Locality']
        self.Pincode = data['Pincode']
        self.City = data['City']
        self.State = data['State']
        self.Country = data['Country']
        self.Latitude = data['Latitude']
        self.Longitude = data['Longitude']
        self.Mobile = data['Mobile']
        self.Instagram = data['Instagram']
        self.Twitter = data['Twitter']
    def is_valid(self):
        return True
    def to_dict(self):
        return {
            'FirstName': self.FirstName,
            'LastName': self.LastName,
            'Email': self.Email,
            'DOB': self.DOB,
            'AddressLine1': self.AddressLine1,
            'AddressLine2': self.AddressLine2,
            'Locality': self.Locality,
            'Pincode': self.Pincode,
            'City': self.City,
            'State': self.State,
            'Country': self.Country,
            'Latitude': self.Latitude,
            'Longitude': self.Longitude,
            'Mobile': self.Mobile,
            'Instagram': self.Instagram,
            'Twitter': self.Twitter
        }

class PostIncidentForm():
    def __init__(self, data, username):
        self.title = data['Title']
        self.description = data['Description']
        self.longitude = float(data['Longitude'])
        self.latitude = float(data['Latitude'])
        self.author = username
        if (data['IncidentType'] == 'Fire'):
            self.incident_type = 1
        elif (data['IncidentType'] == 'Flood'):
            self.incident_type = 2
        elif (data['IncidentType'] == 'Earthquake'):
            self.incident_type = 3
        elif (data['IncidentType'] == 'Landslide'):
            self.incident_type = 4
        elif (data['IncidentType'] == 'Tsunami'):
            self.incident_type = 5
        elif (data['IncidentType'] == 'Virus and Bacteria'):
            self.incident_type = 6
        elif (data['IncidentType'] == 'Cyclone'):
            self.incident_type = 7
        elif (data['IncidentType']=='Drought'):
            self.incident_type = 8
        elif (data['IncidentType']=='Forest Fire'):
            self.incident_type = 9
        elif (data["IncidentType"]=='Industrial Accident'):
            self.incident_type = 10
        elif (data['IncidentType']=='Tax Fraud'):
            self.incident_type = 11
        elif (data['IncidentType']=='Money Laundering'):
            self.incident_type = 12
        elif (data['IncidentType']=='Theft'):
            self.incident_type = 13
        elif (data['IncidentType']=='Smuggling'):
            self.incident_type = 14
        elif (data['IncidentType']=='CyberCrime'):
            self.incident_type = 15
        elif (data['IncidentType']=='Bribe'):
            self.incident_type = 16
        elif (data['IncidentType']=='Hit and Run'):
            self.incident_type = 17
        elif (data['IncidentType']=='Kidnap'):
            self.incident_type = 18
        elif (data['IncidentType']=='Rape'):
            self.incident_type = 19
        else:
            self.incident_type = 20
        self.time = data['Time']
        self.is_authentic = False
        self.upvotes = 0
        self.downvotes = 0
        self.post_ID = username + datetime.now().strftime("%m%d%Y%H%M%S")
    def is_valid(self):
        if (self.title == '' or self.description == '' or self.longitude == '' or self.latitude == '' or self.author == '' or self.incident_type == '' or self.time == ''):
            return False
        return True
    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'author': self.author,
            'incident_type': self.incident_type,
            'time': self.time,
            'is_authentic': self.is_authentic,
            'upvotes': self.upvotes,
            'downvotes': self.downvotes,
            'post_ID': self.post_ID
        }
    
class PostPropertyForm():
    def __init__(self, data, username):
        self.title = data['Title']
        self.description = data['Description']
        self.longitude = float(data['Longitude'])
        self.latitude = float(data['Latitude'])
        self.author = username
        self.score = 0
        self.pincode = int(data['Pincode'])
        self.city = data['City']
        self.state = data['State']
        self.country = data['Country']
        self.address_line1 = data['AddressLine1']
        self.address_line2 = data['AddressLine2']
        self.post_ID = username + datetime.now().strftime("%m%d%Y%H%M%S")
    def is_valid(self):
        if (self.title == '' or self.description == '' or self.longitude == '' or self.latitude == '' or self.author == '' or self.pincode == '' or self.city == '' or self.state == '' or self.country == '' or self.address_line1 == '' or self.address_line2 == ''):
            return False
        return True
    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'author': self.author,
            'score': self.score,
            'pincode': self.pincode,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'address_line1': self.address_line1,
            'address_line2': self.address_line2,
            'post_ID': self.post_ID
        }
    
class ChangePasswordForm():
    def __init__(self, data):
        self.UserName = data['UserName']
        self.DOB = data['DOB']
        self.new_password = data['newPassword']
        self.confirm_password = data['confirmNewPassword']
    def is_valid(self):
        if (self.UserName == '' or self.DOB == '' or self.new_password == '' or self.confirm_password == ''): 
            return False
        if (self.new_password != self.confirm_password):
            return False
        return True
    
class ForgotPasswordForm():
    def __init__(self, data):
        self.UserName = data['UserName']
        self.DOB = data['DOB']
    def is_valid(self):
        if (self.UserName == '' or self.DOB == ''):
            return False
        return True