from django.urls import path
from .views import RegisterView,UserProfileView,UserProfiles,UserLoginView,ImageUploadView,UploadedImagesView,UserWithImagesView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='sign_up'),
    path('login/', UserLoginView.as_view(), name='log_in'),
    path('profile/<int:user_id>/',UserProfileView.as_view(),name='user_profile'),
    path('profiles/',UserProfiles.as_view(),name='user_profiles'),
    path('image_upload/',ImageUploadView.as_view(),name='upload_images'),
    path('uploaded_images/',UploadedImagesView.as_view(),name="uploaded_images"),
    path('user_data/',UserWithImagesView.as_view(),name="user_data")
    
]