from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Region(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Address(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    street = models.CharField(max_length=100, blank = True, null = True)
    house_num = models.CharField(max_length=10, blank = True, null = True)

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    name = models.CharField(max_length=45, blank=True)
    surname = models.CharField(max_length=45, blank=True)
    main_phone = models.CharField(max_length=20, blank=True)
    alternate_phone = models.CharField(max_length=20, blank=True)
    avatar = models.FileField(null=True)
    
    address = models.OneToOneField(Address, blank = True, null = True, on_delete = models.SET_NULL)
    user_type = models.ForeignKey('User_type', blank=True, null=True, on_delete = models.SET_NULL)
    
    
    def __str__(self):
        return self.user.username + ' - ' + self.user.email
    
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class User_type(models.Model):
    name = models.CharField(max_length=45)
    
    def __str__(self):
        return self.name

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.CharField(max_length=80, blank = True, null = True)
    
class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.CharField(max_length=80, blank = True, null = True)
    receiver =  models.CharField(max_length=80, blank = True, null = True)
    
    message = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add = True)

class Report_type(models.Model):
    title = models.CharField(max_length=100)
    label_title = models.CharField(max_length=200, null = True)
    
    def __str__(self):
        return self.label_title


class Report(models.Model):
    created = models.DateTimeField(auto_now_add = True)
    ident_det = models.CharField(max_length=500, blank = True, null = True)
    
    address = models.OneToOneField(Address, blank = True, null = True, on_delete = models.SET_NULL)
    report_type = models.ForeignKey(Report_type, blank=True, null=True, on_delete = models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ForeignKey('Pet', blank=True, null=True, on_delete = models.SET_NULL)
    
    
class Coat(models.Model):
    coat_title = models.CharField(max_length=100)
    length = models.CharField(max_length=50)

class Pet_type(models.Model):
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title
    
class Pet_breed(models.Model):
    breed_title = models.CharField(max_length=100)
    pet_type = models.ForeignKey(Pet_type, on_delete=models.CASCADE)

class Pet(models.Model):
    pet_img = models.FileField(null=True)
    name = models.CharField(max_length=50, blank = True, null = True)
    sex = models.CharField(max_length=20, blank = True, null = True)
    predominant_color = models.CharField(max_length=50, blank = True, null = True)
    height = models.CharField(max_length=20, blank = True, null = True)
    weight = models.CharField(max_length=20, blank = True, null = True)
    age = models.CharField(max_length=20, blank = True, null = True)
    ident_mark_feat = models.CharField(max_length=300, blank = True, null = True)
    collar = models.CharField(max_length=100, blank = True, null = True)
    
    coat = models.ForeignKey(Coat, blank=True, null=True, on_delete = models.SET_NULL)
    pet_type = models.ForeignKey(Pet_type, blank=True, null=True, on_delete = models.SET_NULL)
    pet_breed = models.ForeignKey(Pet_breed, blank=True, null=True, on_delete = models.SET_NULL)