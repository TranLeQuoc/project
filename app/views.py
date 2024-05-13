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
            serializer.save()
            
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
        books = Book.objects.all().order_by('rating')
        serializer = self.serializer_class(books, many=True)
        
        # Modify the serialized data to include the ID
        serialized_data = serializer.data
        for idx, book_data in enumerate(serialized_data):
            book_data['id'] = books[idx].id  # Add 'id' key with the book ID
            
        return Response(serialized_data, status=status.HTTP_200_OK)
    
    
class BookContentView(APIView):
    def get_first_5000_words(self, book_url):
        # Fetch the content of the book file from Cloudinary
        file_url, _ = cloudinary_url(book_url)
        with urllib.request.urlopen(file_url) as response:
            book_content = response.read().decode('utf-8')

        # Extract the first 5000 words
        words = re.findall(r'\b\w+\b', book_content)
        first_5000_words = ' '.join(words[:5000])

        return first_5000_words

    def get(self, request, book_id):
        try:
            # Retrieve the Book instance
            book = Book.objects.get(pk=book_id)
            book_url = book.book_url

            # Get the first 5000 words of the book
            first_5000_words = self.get_first_5000_words(book_url)

            return Response({'first_5000_words': first_5000_words}, status=status.HTTP_200_OK)
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
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Check if the record already exists for the given shelf, user, and book
            shelf_id = serializer.validated_data['shelf_id']
            user_id = serializer.validated_data['user_id']
            book_id = serializer.validated_data['book_id']
            try:
                added_book = AddedBook.objects.get(shelf_id=shelf_id, user_id=user_id, book_id=book_id)
                serializer = self.serializer_class(added_book, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except AddedBook.DoesNotExist:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
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