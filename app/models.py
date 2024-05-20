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
    rating = models.FloatField(default=0.0)
    summary = models.TextField()
    total_pages = models.PositiveIntegerField()
    image_url = models.URLField()
    book_url = models.URLField()
    original_font_size = models.PositiveIntegerField( default = 10)
  
  
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
    image_url = models.URLField(default="https://encrypted-tbn3.gstatic.com/images?q=tbn%3AANd9GcS8OUabGQMxidI9ZxjReu3uqZN2Mos32YWdt_dBiixg7Z8H_LG1")
    user_id = models.IntegerField()
    
class AudioFile(models.Model):
    folder_id = models.IntegerField()
    user_id = models.IntegerField()
    name = models.CharField(max_length=100)
    file_url = models.CharField(max_length=1000,default="https://encrypted-tbn3.gstatic.com/images?q=tbn%3AANd9GcS8OUabGQMxidI9ZxjReu3uqZN2Mos32YWdt_dBiixg7Z8H_LG1")

class Rating(models.Model):
    user_id = models.IntegerField()
    book_id = models.IntegerField()
    rating = models.IntegerField()
    class Meta:
        # Define the combination of shelf_id, user_id, and book_id as the primary key
        unique_together = ('user_id', 'book_id')
        
class ReaderInfo(models.Model):
  reader_id = models.IntegerField(unique=True, default=0)
  email = models.CharField(max_length=30, unique=True)
  first_name = models.CharField(max_length=30, default=" ")
  last_name = models.CharField(max_length=30, default=" ")
  phone_number = models.CharField(max_length=20, default=" ")
  biography = models.TextField(default=" ")
  avatar_url = models.URLField(default="https://cdn-icons-png.flaticon.com/512/1459/1459381.png")
  page_count = models.IntegerField(default=0)
  font_size = models.IntegerField(default=12)
  font_style = models.CharField(max_length=50, default="Arial")
  default_narrator = models.IntegerField(default=0)
    
class ReadingProcess(models.Model):
  user_id = models.IntegerField()
  book_id = models.IntegerField()
  current_page = models.PositiveIntegerField()
  last_update_date = models.DateTimeField(auto_now=True)
  class Meta:
        # Define the combination of shelf_id, user_id, and book_id as the primary key
      unique_together = ('user_id', 'book_id')