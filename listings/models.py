from django.db import models
from django.contrib.auth.hashers import make_password
# Create your models here.
class House(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    location = models.CharField(max_length=100)
    bedrooms = models.IntegerField()
    image = models.ImageField(upload_to='house_images/')
    contact = models.CharField(max_length=10)
    booked = models.BooleanField(default=False)
    booked_by = models.EmailField(blank=True, null=True)
    
    def __str__(self):
        return self.title


class CustomUser(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Store hashed passwords

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)  # Hash the password before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email