from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegistrationSerializer,UserProfileSerializer,UserLoginSerializer,ImageSerializer,UserSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from .models import User,Images



def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class RegisterView(APIView):
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = get_tokens_for_user(user)
    return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)
  
class UserLoginView(APIView):
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data.get('username')
    password = serializer.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
      token = get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Username or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
  
class UserProfileView(APIView):

  def get(self, request, user_id, format=None):
        try:
           user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
  

class UserProfiles(APIView):
   def get(self, request, format=None):
        users = User.objects.filter(is_admin = False)
        serializer = UserProfileSerializer(users,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
   

class ImageUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [ IsAuthenticated ]

    def post(self, request, format=None):
        serializer = ImageSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            print("Inside image upload view : ", request.user)
            serializer.save(user=request.user)  # Link the image to the current user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UploadedImagesView(APIView):
   def get(self, request , format = None):
      all_images = Images.objects.all()
      serializer = ImageSerializer(all_images,many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)
   
class UserWithImagesView(APIView):
    def get(self, request, format=None):
        users = User.objects.filter(is_admin=False)
        serialized_data = []

        for user in users:
            serialized_user = UserSerializer(user).data
            serialized_user['images'] = ImageSerializer(user.images_set.all(), many=True).data
            serialized_data.append(serialized_user)

        return Response(serialized_data)
