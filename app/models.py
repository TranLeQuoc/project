from django.db import models

# Create your models here.
class React(models.Model):
  employee = models.CharField(max_length=30)
  department = models.CharField(max_length=200)
  

class User(models.Model):
  username = models.CharField(max_length=30, unique=True)
  email = models.CharField(max_length=30)
  password = models.CharField(max_length=200)
      
      
      
      
# class User(models.Model):
#     userID = models.CharField(max_length=50, unique=True, primary_key=True)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.EmailField(max_length=254)
#     phone_number = models.CharField(max_length=20)
#     biography = models.TextField()
#     avatar_url = models.URLField(max_length=200)
#     page_count = models.IntegerField()
#     font_size = models.IntegerField()
#     font_style = models.CharField(max_length=50)
#     hashed_password = models.CharField(max_length=100)
    
#     def save(self, *args, **kwargs):
#         if not self.userID:
#             # Generate a unique userID if it's not provided
#             # You can implement your own logic to generate the userID here
#             # For example, you can use UUID or some other unique identifier
#             self.userID = generate_unique_user_id()  # Implement this function
#         super().save(*args, **kwargs)