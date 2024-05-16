import os
import re
from django.http import JsonResponse
from rest_framework.views import APIView
import urllib3
from . models import *
from rest_framework.response import Response
from . serializer import *
from rest_framework import status
import cloudinary
from cloudinary.utils import cloudinary_url
import urllib.request 
from django.db.models import Avg
from django.db.models import Count

# Create your views here.

####################################################    TEST    ######################################################################  

class ReactView(APIView):

    serializer_class = ReactSerializer

    def get(self, request):
        output = [{"employee": output.employee, "department": output.department}
                  for output in React.objects.all()]
        return Response(output)

    def post(self, request):

        serializer = ReactSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
class UserView(APIView):

    serializer_class = UserSerializer

    def get(self, request):
        output = [{"username": user.username, "email": user.email}
                  for user in User.objects.all()]
        return Response(output)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
####################################################    READER/USER    ######################################################################  

class ReaderLoginView(APIView):
    serializer_class = ReaderSerializer

    def get(self, request):
        output = [{"id": reader.id, "email": reader.email} for reader in Reader.objects.all()]
        return Response(output)

    def post(self, request):
        # Get email and password from request data
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Check if account exists
        try:
            reader = Reader.objects.get(email=email, password=password)
        except Reader.DoesNotExist:
            # If account does not exist, return error response
            return Response({"error": "Account does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        # If account exists, return success response with user's id and email
        return Response({"message": "Login successful.", "user_id": reader.id, "email": reader.email}, status=status.HTTP_200_OK)


class ReaderRegisterView(APIView):
    serializer_class = ReaderSerializer

    def post(self, request):
        # Deserialize the request data using the serializer
        serializer = self.serializer_class(data=request.data)
        
        # Check if the data is valid
        if serializer.is_valid():
            # Save the new user to the database
            reader = serializer.save()
            
            reader_info = ReaderInfo(
                reader_id=reader.id,
                email=reader.email
            )
            reader_info.save()
            # Return success response
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        else:
            # If the data is not valid, return error response with validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
####################################################    BOOK    ######################################################################  
        
class BookView(APIView):
    serializer_class = BookSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        books = Book.objects.all().order_by('-rating')
        serializer = self.serializer_class(books, many=True)
        
        # Modify the serialized data to include the ID
        serialized_data = serializer.data
        for idx, book_data in enumerate(serialized_data):
            book_data['id'] = books[idx].id  # Add 'id' key with the book ID
            
        return Response(serialized_data, status=status.HTTP_200_OK)
    
class BookByPopularView(APIView):
    serializer_class = BookSerializer

    def get(self, request):
        # Get all books
        books = Book.objects.all()

        # List to store tuples of book objects and their corresponding counts
        books_with_counts = []

        # Loop through each book
        for book in books:
            # Count the number of ratings for the current book
            rating_count = Rating.objects.filter(book_id=book.id).count()
            # Append tuple of book object and its rating count to the list
            books_with_counts.append((book, rating_count))

        # Sort the books based on the rating counts in descending order
        sorted_books_with_counts = sorted(books_with_counts, key=lambda x: x[1], reverse=True)

        # Extract sorted books from the sorted list
        sorted_books = [book_count[0] for book_count in sorted_books_with_counts]

        # Serialize the sorted books
        serializer = self.serializer_class(sorted_books, many=True)

        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class BookDetailView(APIView):
    serializer_class = BookSerializer

    def get(self, request, book_id):
        try:
            book = Book.objects.get(pk=book_id)
            serializer = self.serializer_class(book)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        
class BookContentView(APIView):
    def get_content(self, book_url, beginIdx):
        begin_index = beginIdx * 5000
        # Fetch the content of the book file from Cloudinary
        file_url, _ = cloudinary_url(book_url)
        with urllib.request.urlopen(file_url) as response:
            book_content = response.read().decode('utf-8')

        # Extract the first 5000 characters
        selected_characters = book_content[begin_index:begin_index + 5000]

        return selected_characters

    def get(self, request, book_id,page_number = 0):
        try:
            # Retrieve the Book instance
            book = Book.objects.get(pk=book_id)
            book_url = book.book_url

            # Get the first 5000 words of the book
            content_page = self.get_content(book_url,page_number)

            response_key = f'content_page_{page_number + 1}'

            return Response({response_key: content_page}, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        
def getPathOS(request):
    
    return JsonResponse({'osLink': os.getcwd()})

def upload_text_file(fileName):
    # Upload the text file to Cloudinary
    file_path = os.path.join(os.getcwd(), "resources", "books", fileName)
    upload_result = cloudinary.uploader.upload(file_path, resource_type="raw")

    # Return the public URL of the uploaded text file
    return upload_result["url"]

def BookUploading(request, book_id, fileName):
    try:
        # Get the Book instance by ID
        book = Book.objects.get(pk=book_id)

        # Upload the text file to Cloudinary
        public_url = upload_text_file(fileName)

        # Update the book_url field of the Book instance
        book.book_url = public_url
        book.save()

        return JsonResponse({'uploaded_link': public_url})
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)
    
    
    
####################################################    SHELF    ######################################################################  

class ShelfView(APIView):
    serializer_class = ShelfSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, user_id=None):  # Add user_id=None as a default parameter
        if user_id is not None:
            shelves = Shelf.objects.filter(user_id=user_id)
        else:
            shelves = Shelf.objects.all()
            
        serializer = self.serializer_class(shelves, many=True)
        
        # Modify the serialized data to include the ID
        serialized_data = serializer.data
        for idx, shelf_data in enumerate(serialized_data):
            shelf_data['id'] = shelves[idx].id  # Add 'id' key with the shelf ID
            
        return Response(serialized_data)
        

####################################################    ADDEDBOOK    ######################################################################  

class AddedBookView(APIView):
    serializer_class = AddedBookSerializer
    
    def post(self, request):
        data = request.data
        shelf_id = data.get('shelf_id')
        user_id = data.get('user_id')
        book_id = data.get('book_id')
        
        try:
            # Try to fetch the existing object
            added_book = AddedBook.objects.get(shelf_id=shelf_id, user_id=user_id, book_id=book_id)
            serializer = self.serializer_class(added_book, data=data, partial=True)
        except AddedBook.DoesNotExist:
            # If the object does not exist, create a new one
            serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            status_code = status.HTTP_200_OK if 'id' in serializer.data else status.HTTP_201_CREATED
            return Response(serializer.data, status=status_code)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, shelf_id=None, user_id=None):
        if user_id:
            if shelf_id:
                added_books = AddedBook.objects.filter(shelf_id=shelf_id, user_id=user_id)
            else:
                added_books = AddedBook.objects.filter(user_id=user_id)
                
            # Sort added books based on last_update_date in descending order
            added_books = added_books.order_by('-last_update_date')
            
            serialized_books = []
            for added_book in added_books:
                book = Book.objects.get(pk=added_book.book_id)  # Fetch associated book
                book_serializer = BookSerializer(book)  # Serialize associated book
                added_book_data = AddedBookSerializer(added_book).data  # Serialize added book
                added_book_data['book'] = book_serializer.data  # Add serialized book data to added book data
                serialized_books.append(added_book_data)
                
            return Response(serialized_books, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        
####################################################    AUDIO FOLDER    ######################################################################  

class AudioFolderView(APIView):
    serializer_class = AudioFolderSerializer

    def post(self, request):
        folder_id = request.data.get('id')  # Get the ID from the request data
        if folder_id:
            try:
                # Check if the folder with the provided ID exists
                folder = AudioFolder.objects.get(pk=folder_id)
                # If the folder exists, update it with the request data
                serializer = self.serializer_class(folder, data=request.data)
            except AudioFolder.DoesNotExist:
                # If the folder does not exist, create a new one
                serializer = self.serializer_class(data=request.data)
        else:
            # If no ID is provided, create a new folder
            serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            # Save the folder to the database
            serializer.save()
            # Return the ID of the created or modified folder
            return Response({'id': serializer.data['id']}, status=status.HTTP_201_CREATED)
        else:
            # If the data is not valid, return error response with validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id = None):
        try:
            # Get the audio folder instance by ID
            folder = AudioFolder.objects.get(pk=id)
            folder.delete()
            return Response({'message': 'Audio folder deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except AudioFolder.DoesNotExist:
            return Response({'error': 'Audio folder not found'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, user_id=None):
        if user_id is not None:
            # Retrieve all audio folders with the specified user_id
            audio_folders = AudioFolder.objects.filter(user_id=user_id)
        else:
            # Retrieve all audio folders if user_id is None
            audio_folders = AudioFolder.objects.all()
        # Serialize the retrieved audio folders
        serializer = self.serializer_class(audio_folders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
####################################################    AUDIO FILE    ######################################################################  

class AudioFileView(APIView):
    serializer_class = AudioFileSerializer

    def post(self, request):
        audio_file_id = request.data.get('id')

        if audio_file_id:
            try:
                # Check if the audio file exists
                audio_file = AudioFile.objects.get(pk=audio_file_id)
                serializer = self.serializer_class(audio_file, data=request.data)
            except AudioFile.DoesNotExist:
                return Response({'error': 'Audio file not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, audio_file_id):
        try:
            audio_file = AudioFile.objects.get(pk=audio_file_id)
            audio_file.delete()
            return Response({'message': 'Audio file deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except AudioFile.DoesNotExist:
            return Response({'error': 'Audio file not found'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, user_id=None, folder_id=None):
        if user_id is not None:
            if folder_id is not None:
                audio_files = AudioFile.objects.filter(user_id=user_id, folder_id=folder_id)
            else:
                audio_files = AudioFile.objects.filter(user_id=user_id)
        else:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(audio_files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RatingView(APIView):
    serializer_class = RatingSerializer

    def post(self, request):
        user_id = request.data.get('user_id')
        book_id = request.data.get('book_id')
        rating_value = request.data.get('rating')

        try:
            # Try to get the existing rating for the user and book
            rating = Rating.objects.get(user_id=user_id, book_id=book_id)
            rating.rating = rating_value  # Update the rating value
            rating.save()
        except Rating.DoesNotExist:
            # If no rating exists, create a new one
            rating = Rating.objects.create(user_id=user_id, book_id=book_id, rating=rating_value)

        # Recalculate the average rating for the book
        average_rating = Rating.objects.filter(book_id=book_id).aggregate(Avg('rating'))['rating__avg']
        # Update the average rating in the corresponding Book instance
        book = Book.objects.get(pk=book_id)
        book.rating = average_rating
        book.save()

        return Response({'message': 'Rating updated successfully'}, status=status.HTTP_200_OK)

    def get(self, request, user_id=None, book_id=None):
        if user_id is None or book_id is None:
            return Response({'error': 'User ID and Book ID are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Try to get the rating for the user and book
            rating = Rating.objects.get(user_id=user_id, book_id=book_id)
            serializer = self.serializer_class(rating)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Rating.DoesNotExist:
            return Response({'rating': 0}, status=status.HTTP_200_OK)
        
####################################################    ReaderInfo    ######################################################################  


class ReaderInfoCreateView(APIView):
    serializer_class = ReaderInfoSerializer

    def post(self, request):
        # Deserialize the request data using the serializer
        serializer = self.serializer_class(data=request.data)
        
        # Check if the data is valid
        if serializer.is_valid():
            # Save the new ReaderInfo to the database
            serializer.save()
            
            # Return success response
            return Response({"message": "ReaderInfo created successfully."}, status=status.HTTP_201_CREATED)
        else:
            # If the data is not valid, return error response with validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ReaderInfoByEmailView(APIView):
    serializer_class = ReaderInfoSerializer

    def get(self, request, email):
        try:
            reader_info = ReaderInfo.objects.get(email=email)
            serializer = self.serializer_class(reader_info)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ReaderInfo.DoesNotExist:
            return Response({"error": "ReaderInfo not found."}, status=status.HTTP_404_NOT_FOUND)

class ReaderInfoByIdView(APIView):
    serializer_class = ReaderInfoSerializer

    def get(self, request, reader_id):
        try:
            reader_info = ReaderInfo.objects.get(reader_id=reader_id)
            serializer = self.serializer_class(reader_info)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ReaderInfo.DoesNotExist:
            return Response({"error": "ReaderInfo not found."}, status=status.HTTP_404_NOT_FOUND)
        
class ReaderChangeInfo(APIView):
    serializer_class = ReaderInfoSerializer

    def post(self, request):
        try:
            reader_info = ReaderInfo.objects.get(reader_id=request.data.get('reader_id'))
        except ReaderInfo.DoesNotExist:
            return Response({"error": "ReaderInfo not found."}, status=status.HTTP_404_NOT_FOUND)

        # Deserialize the request data using the serializer, allowing partial updates
        serializer = self.serializer_class(reader_info, data=request.data, partial=True)

        # Check if the data is valid
        if serializer.is_valid():
            # Save the updated ReaderInfo to the database
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # If the data is not valid, return error response with validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

