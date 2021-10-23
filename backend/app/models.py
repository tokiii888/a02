# from django.db import models

# # Create your models here.

# class User(models.Model):
#     # user_id = models.AutoField(primary_key=True) #id
#     user_name = models.CharField(max_length=30, null=False) #name
#     email_address = models.EmailField(null=False) #mail adress
#     token = models.CharField(max_length=100,null=False) #token
#     task_count = models.IntegerField(default=0, null=False) #today's task count
#     is_notification = models.BooleanField(default=True, null=False) #notification flag (on/off)
from django.db import models
import django.utils.timezone

from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email: str, password: str, is_staff: bool, is_superuser: bool, **extra_fields):
        """Creates and saves a User with the given email and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField('First Name', max_length=255, blank=True, null=False)
    last_name = models.CharField('Last Name', max_length=255, blank=True, null=False)
    last_login = models.DateTimeField('last login', blank=True, null=True)
    is_superuser = models.BooleanField('superuser status', default=False)
    is_staff = models.BooleanField('staff status', default=False, help_text='Designates whether the user can log into this admin site.')
    is_active = models.BooleanField('active', default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')
    date_joined = models.DateTimeField('date joined', default=django.utils.timezone.now)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} - {self.first_name} {self.last_name}"

class Category(models.Model):
    # category_id = models.AutoField(primary_key=True) #id
    category_name = models.CharField(max_length=30, null=False) #name
    color_code = models.CharField(max_length=7, null=False) #color code (ex. #FF0060)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False) #user id (fk)


class Task(models.Model):
    # task_id = models.AutoField(primary_key=True) #id
    title = models.CharField(max_length=30, null=False) #task title
    detail = models.CharField(max_length=1000, null=True,blank=True) #task detail
    url = models.CharField(max_length=300, null=True,blank=True) #task URL
    created_at = models.DateTimeField(auto_now=True) #create datetime
    priority = models.IntegerField(default=100, null=False) #priority
    next_display_date = models.DateField(null=False) #next display date
    display_times = models.IntegerField(default=0, null=False) #Number of times displayed
    consecutive_times = models.IntegerField(default=0, null=False) #Number of consecutive 2 achievements
    is_update = models.BooleanField(default=True, null=False) #update flag (on/off)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False) #user id (fk)
    category = models.ManyToManyField(Category, through='TaskCategoryRelation')


class TaskCategoryRelation(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class History(models.Model):
    # history_id = models.AutoField(primary_key=True) #id
    completed_date = models.DateField(null=False) #completed date
    feedback = models.IntegerField(default=1, null=False) #feedback number
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False) #user id (fk)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE, null=False) #task id (fk)

class Profile(models.Model):
    username = models.CharField(max_length=30, null=True) #name
    is_notification = models.BooleanField(default=True, null=False) #notification flag (on/off)
    task_limit = models.IntegerField(default=100, null=False) #task display limit
    update_time = models.IntegerField(default=0, null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False) #user id (fk)
