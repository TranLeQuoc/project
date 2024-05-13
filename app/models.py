from django.db import models

# Create your models here.
class React(models.Model):
  employee = models.CharField(max_length=30)
  department = models.CharField(max_length=200)
  

class User(models.Model):
  username = models.CharField(max_length=30, unique=True)
  email = models.CharField(max_length=30)
  password = models.CharField(max_length=200)
      
      
class Reader(models.Model):
  email = models.CharField(max_length=30, unique=True)
  password = models.CharField(max_length=200)

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    rating = models.FloatField()
    summary = models.TextField()
    total_pages = models.PositiveIntegerField()
    image_url = models.URLField()
    book_url = models.URLField()
    original_font_size = models.PositiveIntegerField()
  
  
class Shelf(models.Model):
    name = models.CharField(max_length=100)
    user_id = models.IntegerField()
  
  
class AddedBook(models.Model):
    shelf_id = models.IntegerField()
    user_id = models.IntegerField()
    book_id = models.IntegerField()
    added_date = models.DateTimeField(auto_now_add=True)
    current_page = models.IntegerField(default=0)
    last_update_date = models.DateTimeField(auto_now=True)

    class Meta:
        # Define the combination of shelf_id, user_id, and book_id as the primary key
        unique_together = ('shelf_id', 'user_id', 'book_id')
  
class AudioFolder(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    image_url = models.URLField()
    user_id = models.IntegerField()
    
class AudioFile(models.Model):
    folder_id = models.IntegerField()
    user_id = models.IntegerField()
    name = models.CharField(max_length=100)
    file_url = models.URLField()

class Rating(models.Model):
    user_id = models.IntegerField()
    book_id = models.IntegerField()
    rating = models.IntegerField()
    class Meta:
        # Define the combination of shelf_id, user_id, and book_id as the primary key
        unique_together = ('user_id', 'book_id')
        
        
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