from rest_framework.views import APIView
from . models import *
from rest_framework.response import Response
from . serializer import *
from rest_framework import status


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
        
class ReaderView(APIView):

    serializer_class = ReaderSerializer

    def get(self, request):
        output = [{"email": reader.email}
                  for reader in Reader.objects.all()]
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
        
        # If account exists, return success response
        return Response({"message": "Login successful.", "user's email": reader.email}, status=status.HTTP_200_OK)