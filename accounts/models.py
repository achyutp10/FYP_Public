import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import Point



# Create your models here.
class UserManager(BaseUserManager):
  def create_user(self, first_name, last_name, username, email, phone_number, profile_picture, password=None):
    if not email:
      raise ValueError('Users must have an email address')

    if not username:
      raise ValueError('User must have a username')
    
    user = self.model(
      email = self.normalize_email(email),
      username = username,
      user_id = uuid.uuid4(),
      first_name = first_name,
      last_name = last_name,
      phone_number=phone_number,
      profile_picture=profile_picture,
    )
    user.set_password(password)
    user.save(using=self._db)
    return user
  
  def create_superuser(self, first_name, last_name, username, email, phone_number=None, profile_picture=None, password=None):
    user = self.create_user(
      email=self.normalize_email(email),
      username=username,
      password=password,
      first_name=first_name,
      last_name=last_name,
      phone_number=phone_number,
      profile_picture=profile_picture,
    )
    user.is_admin = True
    user.is_active = True
    user.is_staff = True
    user.is_superadmin = True
    user.is_superuser = True
    user.save(using=self._db)
    return user

from django.utils.deconstruct import deconstructible

@deconstructible
class UserImagePath:
    def __init__(self, sub_path):
        self.sub_path = sub_path

    def __call__(self, instance, filename):
        # Generate the path and filename
        return f'users/profile_pictures/{instance.username}/{filename}'
class User(AbstractBaseUser):
  TECHNICIAN = 1
  CUSTOMER = 2

  ROLE_CHOICES = (
    (TECHNICIAN, 'Technician'),
    (CUSTOMER, 'Customer'),
  )

  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  username = models.CharField(max_length=50, unique=True)
  user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
  profile_picture = models.ImageField(upload_to=UserImagePath('profile_pictures'), blank=True, null=True)
  email = models.EmailField(max_length=100, unique=True)
  phone_number = models.CharField(max_length=12, blank=True, null=True)
  role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)

  # Required fields
  date_joined = models.DateTimeField(auto_now_add=True)
  last_login = models.DateTimeField(auto_now_add=True)
  created_date = models.DateTimeField(auto_now_add=True)
  modified_date = models.DateTimeField(auto_now=True)
  is_admin = models.BooleanField(default=False)
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=False)
  is_superadmin = models.BooleanField(default=False)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

  objects = UserManager()

  def __str__(self):
    return self.email
  
  def has_perm(self,perm,obj=None):
    return self.is_admin
  
  def has_module_perms(self, app_label):
    return True
  
  def get_role(self):
    if self.role == 1:
      user_role = 'Technician'
    elif self.role == 2:
      user_role = 'Customer'
    return user_role

class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
  address = models.CharField(max_length=250, blank=True, null=True)
  country = models.CharField(max_length=150, blank=True, null=True)
  state = models.CharField(max_length=150, blank=True, null=True)
  city = models.CharField(max_length=150, blank=True, null=True)
  pin_code = models.CharField(max_length=6, blank=True, null=True)
  latitude = models.CharField(max_length=20, blank=True, null=True)
  longitude = models.CharField(max_length=20, blank=True, null=True)
  location = gismodels.PointField(blank=True, null=True, srid=4326)
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now=True)
    
  def __str__(self):
    return self.user.email
  
  def save(self, *args, **kwargs):
    if self.latitude and self.longitude:
      self.location = Point(float(self.longitude), float(self.latitude))
      return super(UserProfile, self).save(*args, **kwargs)
    return super(UserProfile, self).save(*args, **kwargs)
  

