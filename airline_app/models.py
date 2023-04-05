from django.db import models
 
# Create your models here
class Customer(models.Model):
    fullname = models.TextField(max_length=50)
    username = models.TextField(max_length=50)
    email = models.TextField(max_length=50)
    contact = models.TextField(max_length=50)
    password = models.TextField(max_length=50)
    city = models.TextField(max_length=50)
    date_of_birth = models.DateField()
    image = models.ImageField(upload_to='pictures/')
    gender = models.TextField(max_length=50)

class Request(models.Model):
    name = models.TextField(max_length=50)
    username = models.TextField(max_length=50)
    email = models.TextField(max_length=50)
    contact = models.TextField(max_length=50)
    password = models.TextField(max_length=50)
    country = models.TextField(max_length=50)
    image = models.ImageField(upload_to='pictures/')

class Airlines(models.Model):
    name = models.TextField(max_length=50)
    username = models.TextField(max_length=50)
    email = models.TextField(max_length=50)
    contact = models.TextField(max_length=50)
    password = models.TextField(max_length=50)
    country = models.TextField(max_length=50)
    image = models.ImageField(upload_to='pictures/')

class Admin(models.Model):
    username = models.TextField(max_length=50)
    password = models.TextField(max_length=50)
    
class Flight(models.Model):
    airline_name = models.TextField(max_length=50)
    flight_no = models.TextField(max_length=50)
    departure_city = models.TextField(max_length=50)
    arrival_city = models.TextField(max_length=50)
    departure_datetime = models.DateTimeField()
    arrival_datetime = models.DateTimeField()
    no_of_seats = models.TextField(max_length=50)
    price = models.TextField(max_length=50)
    image = models.ImageField(upload_to='pictures/')

class Feedback(models.Model):
    name = models.TextField(max_length=50)
    email = models.TextField(max_length=50)
    date = models.DateField()
    message = models.TextField(max_length=50)
    
class ImageUpload(models.Model):
    airline_name = models.TextField(max_length=50)
    flight_no = models.TextField(max_length=50)
    image = models.ImageField(upload_to='pictures/')