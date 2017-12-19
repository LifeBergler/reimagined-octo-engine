from __future__ import unicode_literals
import re
import bcrypt
from datetime import datetime
from django.db import models

# Create your models here.

class UserManager(models.Manager):
  # validates the login data
  def validate_login(self, postData):
    results = {'status': True, 'errors': [], 'user' : None}
    users = self.filter(email = postData['email'])
    # checks if the email is in the database
    if len(users) < 1:
      results['status'] = False
      results['errors'].append('Not a registered email')
    else:
      if bcrypt.checkpw(postData['password'].encode(), users[0].password.encode()):
        results['user'] = users[0]
      else:
        results['status'] = False
    return results
  # creates the user when registered
  def creator(self, postData):
    user = self.create(first_name = postData['first_name'], last_name = postData['last_name'], email = postData['email'], password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()))
    return user  
  def validate(self, postData):
    results = {'status': True, 'errors': []}
    if len(postData['first_name']) < 3:
      results['errors'].append('First name must be at least 2 characters')
      results['status'] = False
    if len(postData['last_name']) < 2:
      results['errors'].append('Last name must be at least 2 characters')
      results['status'] = False
    if not re.match("[^@]+@[^@]+\.[^@]+", postData['email']):
      results['errors'].append('Not a valid email address')
      results['status'] = False
    if len(postData['password']) < 8:
      results['errors'].append('Password must be at least 8 characters')
      results['status'] = False
    if postData['password'] != postData['c_password']:
      results['errors'].append('Passwords do not match')
      results['status'] = False
    if len(self.filter(email = postData['email'])) > 0:
      results['errors'].append('User already exists')
      results['status'] = False
    return results
  
    
# User class
class User(models.Model):
  first_name = models.CharField(max_length = 255)
  last_name = models.CharField(max_length = 255)
  email = models.CharField(max_length = 255)
  password  = models.CharField(max_length = 255)
  objects = UserManager()

# Trip Manager class
class TripManager(models.Manager):
  results = {'status': True, 'errors': []}
  def creator_trip(self, postData):
    trip = self.create(destination = postData['destination'], description = postData['description'], travel_date_from = postData['travel_date_from'], travel_date_to = postData['travel_date_to'], user_id = postData['user_id'])
    return trip
  def validate_trip(self, postData):
    # -- trying to validate the dates given in the "add plan" form.  date_to must be greater than date_from, and both dates must be in the future --
    # past = datetime.now()
    present = datetime.now().strftime("%Y-%m-%d")
    date_from = postData['travel_date_from']
    date_to = postData['travel_date_to']
    
    print '*'*50
    print present
    print date_from
    print date_to
    print '*'*50
    # new_date_from = time.strptime(date_from, "%d/%m/%Y")
    # new_date_to = time.strptime(date_from, "%d%m%Y")
    
    results = {'status' : True, 'errors' : [], 'trip' : None}
    if len(postData['destination']) < 2:
      results['errors'].append('Destination must be at least 2 characters')
      results['status'] = False
    if len(postData['description']) < 2:
      results['errors'].append('Description must be at least 2 characters')
      results['status'] = False
    if date_from > date_to:
      results['errors'].append("Departure date must be before return date")
      results['status'] = False
    if present > date_from or present > date_to:
      results['errors'].append("Dates must be in the future, dummy")
      results['status'] = False
      # be sure to come back and validate ur datetiiiiiiiiiiimes :)********************************************************************************************************************************************************************************************
    return results

# Trip class
class Trip(models.Model):
  destination = models.CharField(max_length = 255)
  description = models.CharField(max_length = 500)
  user = models.ForeignKey(User, related_name = "trips")
  joined_by = models.ManyToManyField(User, related_name="trips_joined")
  travel_date_from = models.DateTimeField(verbose_name=None)
  travel_date_to = models.DateTimeField(verbose_name=None)
  objects = TripManager()