from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from models import *
# Create your views here.

#  "/"
def index(request):
  return render(request, 'login_app/index.html')

# "/register"
def register(request):
  results = User.objects.validate(request.POST)
  if results['status'] is True:
    user = User.objects.creator(request.POST)
    messages.success(request, "User has been registered")
  else:
    for error in results['errors']:
      messages.error(request, error)
  return redirect('/')

# "/login"
def login(request):
  results = User.objects.validate_login(request.POST)
  if results['status'] is False:
    messages.error(request, "Email and password do not match")
    return redirect('/')
  request.session['email'] = results['user'].email
  request.session['first_name'] = results['user'].first_name
  request.session['user_id'] = results['user'].id
  return redirect('/dashboard')

# "/dashboard"
def dashboard(request):
  if 'email' not in request.session:
    return redirect('/')
  user = User.objects.get(id=request.session['user_id'])
  context = {
    'trips' : Trip.objects.filter(joined_by = user),
    'other_trips' : Trip.objects.exclude(joined_by = user)
  }
  return render(request, "login_app/dashboard.html", context)

# "/logout"
def logout(request):
  # b = User.objects.all()
  # b.delete() # deletes that particular record
  request.session.flush()
  return redirect('/')

# "/add_plan"
def add_plan(request):
  return render(request, "login_app/add_plan.html")

# "/create" (creates the plan to be added)
def create_trip(request):
  print request.POST
  results = Trip.objects.validate_trip(request.POST)
  if results['status'] is True:
    trip = Trip.objects.creator_trip(request.POST)
    messages.success(request, "Trip has been added!")
    return redirect('/dashboard')
  else: 
    for error in results['errors']:
      messages.error(request, error)
    return redirect('/add_plan')

# "/join/<trip_id>" (joins another user's trip to your joined_trips table or i dunno wtf it's called)
def join(request, trip_id):
  user = User.objects.get(id = request.session['user_id'])
  trip = Trip.objects.get(id = trip_id)
  trip.joined_by.add(user)
  trip.save()
  return redirect('/dashboard')

# "/info/<id>" clicking on a destination link from the dashboard will bring you here.  Just pass the trip info w/ trip_id and joined_by_id to the "info.html" and use the jinja to show it plz.
def info(request, trip_id):
  trip = Trip.objects.get(id = trip_id)
  context = {
    'trip' : trip,
    'users' : User.objects.filter(trips_joined = trip).exclude(id = trip.user.id)
  }
  print '*'*50
  print trip.destination
  # print user.id
  print '*'*50
  return render(request, 'login_app/info.html', context)

# -- I want this to remove the selected trip from the logged in user's planned trips
def untrip(request, trip_id):
  user = User.objects.get(id = request.session['user_id'])
  trip = Trip.objects.get(id = trip_id)
  trip.joined_by.remove(user)
  trip.save()
  return redirect('/dashboard')