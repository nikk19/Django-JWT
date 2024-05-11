from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username , user_name, password=None, password2 = None):
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            username=username,
            user_name=user_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, user_name=None, password=None):
        user = self.create_user(
            username=username,
            password=password,
            user_name=user_name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    USER_TYPE_CHOICES = [
        ('private', 'Private'),
        ('public', 'Public')
    ]

    username = models.CharField(max_length=150, unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='private')
    user_name = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['user_name']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
      # Simplest possible answer: All admins are staff
      return self.is_admin
    

def user_directory_path(instance, filename):
    username =instance.user.user_name
    return f'user_images/{username}/{filename}'
    
class Images(models.Model):
    image = models.ImageField(upload_to=user_directory_path)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
