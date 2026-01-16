from django.db import models
from django.conf import settings
from .choices import RATE_CHOICES 
from taggit.managers import TaggableManager

class Subject(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Review(models.Model):
    # Updated: Changed 'shop.Product' to 'pages.Product' 
    # This connects the Review to the Product class in your pages app.
    product = models.ForeignKey(
        'pages.Product', 
        on_delete=models.CASCADE, 
        related_name='reviews'
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    
    content = models.TextField(max_length=500)
    # rating = models.IntegerField(choices=rate_choice, default=5)
    rating = models.IntegerField(choices=RATE_CHOICES, default=5)
    
    # Using taggit to categorize reviews (e.g. "Tasty", "Value for money")
    tags = TaggableManager()
    
    # sets the date when the object is first created
    created_at = models.DateTimeField(auto_now_add=True)
    
    # the field to the current timestamp every single time the save() method is called
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        # This will now correctly pull the 'name' from pages/models.py Product class
        return f"Review for {self.product.name} by {self.user.username}"

    def tag_list(self):
        return u', '.join(tag.name for tag in self.tags.all())