from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class UserManager(BaseUserManager):

    def _create_user(self, first_name, last_name, username, email, password, is_staff, is_superuser, birthdate, age, phone, gender, **extra_fields):

        user = self.model(
            last_name=last_name,
            first_name=first_name,
            username=username,
            email=self.normalize_email(email),
            is_staff=is_staff,
            is_superuser=is_superuser,
            birthdate=birthdate,
            age=age,
            phone=phone,
            gender=gender
        )

        user.set_password(password)
        user.save(using=self.db)

        return user
    
    def create_user(self, first_name, last_name, username, email, password=None, **extra_fields):
        return self._create_user(first_name, last_name, username, email, password, False, False, **extra_fields)
    
    def create_superuser(self, first_name, last_name, username, email, password=None, **extra_fields):
        return self._create_user(first_name, last_name, username, email, password, True, True, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):

    class UserGender(models.TextChoices):

        male = "male"
        female = "female"
        other = "other"

    id_user = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    date_joined = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    birthdate = models.DateField()
    age = models.PositiveSmallIntegerField()
    phone = models.CharField(max_length=18, unique=True)
    gender = models.CharField(max_length=10, choices=UserGender.choices)
    objects = UserManager()

    class Meta:

        db_table = "user"
        verbose_name = "user"
        verbose_name_plural = "users"

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def get_full_name(self):
        return self.first_name + " " + self.last_name
    
    def get_short_name(self):
        return self.first_name
    
    def natural_key(self):
        return (self.username,)
    
    def __str__(self):

        return self.username

class Address(models.Model):

    id_address = models.BigAutoField(primary_key=True)
    name_address = models.CharField(max_length=100)
    street = models.CharField(max_length=40)
    number = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=40)
    region = models.CharField(max_length=60)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:

        db_table = "address"
        verbose_name = "address"
        verbose_name_plural = "addresses"

    def __str__(self):
        return self.name_address
