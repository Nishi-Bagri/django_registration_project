from django.db import models

class CustomUser(models.Model):

    Role_Choices = [
        ('user', 'User'),
        ('admin','Admin'), 
    ]
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)
    phone = models.CharField(max_length=15,blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    house_no = models.CharField(max_length=20, blank=True, null=True)
    street = models.CharField(max_length=225, blank=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    role = models.CharField(max_length=10, choices= Role_Choices, default='user')

    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.png' , null=True, blank=True)
    
    def __str__(self):
        return self.name
