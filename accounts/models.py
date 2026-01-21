
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
import os
# Create your models here.

def profile_image_path(instance, filename):
    """Generate file path for profile image"""
    ext = filename.split('.')[-1]
    filename = f'{instance.id}_{instance.first_name}.{ext}'
    return os.path.join("image/profile_pictures/", filename)

class Profile(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default="image/profile_pictures/profilepic.jpg",
        upload_to="image/profile_pictures",
    )    
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(
        max_length=255,
        unique=True,
        validators=[EmailValidator(message="Enter a valid email address")],
        blank=True,
        null=True        
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(
        default="image/profile_pictures/profilepic.jpg",
        upload_to=profile_image_path,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
   

    def user_name(self):
        return self.user.username
