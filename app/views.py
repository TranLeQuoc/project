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
        
        
        
        
class BookView(APIView):
    serializer_class = BookSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        books = Book.objects.all()
        serializer = self.serializer_class(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    

def get_first_5000_words(book_url):
    # Assuming your book file is a plain text file stored in Cloudinary
    # Fetch the content of the book file from Cloudinary
    file_url, _ = cloudinary_url(book_url)
    with urllib.request.urlopen(file_url) as response:
        book_content = response.read().decode('utf-8')

    # Extract the first 5000 words
    words = re.findall(r'\b\w+\b', book_content)
    first_5000_words = ' '.join(words[:5000])

    return first_5000_words


def BookContentView(request, book_id):
    try:
        # Assuming your Book model has a field named 'book_url' containing the Cloudinary URL of the text file
        book = Book.objects.get(pk=book_id)
        book_url = book.book_url
        first_5000_words = get_first_5000_words(book_url)
        return JsonResponse({'first_5000_words': first_5000_words})
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)
    
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