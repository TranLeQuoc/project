from rest_framework import serializers
from . models import *
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class ReactSerializer(serializers.ModelSerializer):
    class Meta:
        model = React
        fields = ['employee', 'department']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.save()
        return user
    
class ReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = ['email', 'password']
        
    def create(self, validated_data):
        reader = Reader(
            email=validated_data['email'],
            password=validated_data['password']
        )
        reader.save()
        return reader
    
    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid email format")
        return value

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'rating', 'summary', 'total_pages', 'image_url', 'book_url', 'original_font_size']
        
class ShelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shelf
        fields = ['name', 'user_id']

class AddedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddedBook
        fields = ('id', 'shelf_id', 'user_id', 'book_id', 'added_date', 'current_page', 'last_update_date')
        
class AudioFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioFolder
        fields = ['id', 'name', 'category', 'image_url', 'user_id']
        
class AudioFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioFile
        fields = ['id', 'folder_id', 'user_id', 'name', 'file_url']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'user_id', 'book_id', 'rating']
        
class ReaderInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReaderInfo
        fields = ['reader_id', 'email', 'first_name', 'last_name', 'phone_number', 'biography', 'avatar_url', 'page_count', 'font_size', 'font_style']

class ReadingProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingProcess
        fields = ['id', 'user_id', 'book_id', 'current_page']