from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group, Permission
from parler.models import TranslatableModel, TranslatedFields

# Create your models here.


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_At = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', )
        abstract = True
    


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        
        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractUser, TimeStamp):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'Prefer not to say'),
    ]
    
    email = models.EmailField(_("email address"), unique=True)
    full_name = models.CharField(max_length=220)
    country = models.CharField(max_length=220)
    mobile = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='N') 
    role = models.CharField(max_length=20)
    confirmation_code = models.CharField(max_length=220)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        
        if self.role == 'admin':
            self.is_staff = True
        super().save(*args, **kwargs)

        # Add the user to their corresponding group
        try:
            group = Group.objects.get(name=self.role.title())
        except Group.DoesNotExist:
            group = Group.objects.create(name=self.role.title())
        if self.role == 'admin':
            group.permissions.set(Permission.objects.all())
        # else:
        #     group.permissions.add(*self.get_permissions())
        group.user_set.add(self)

    # def get_permissions(self):
    #     # Define the permissions for the user based on their role
    #     if self.role == 'instructor':
    #         return ['add_course', 'change_course', 'delete_course']
    #     elif self.role == 'student':
    #         return ['view_course']

    #     return []

class AdminProfile(TimeStamp):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='admin_profile')
    date_of_hire = models.DateField(auto_now_add=True)
    job_title = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return self.user.email


class StudentProfile(TimeStamp):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    major = models.CharField(max_length=50, null=True, blank=True)
    gpa = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return self.user.email


class InstructorProfile(TimeStamp):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='instructor_profile')
    department = models.CharField(max_length=50)
    teaching_experience = models.IntegerField(default=0)

    def __str__(self):
        return self.user.email


class PartnerProfile(TimeStamp):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='partner_profile')
    
    def __str__(self):
        return self.user.email
    

class TeamMember(TimeStamp, TranslatableModel):
    translations = TranslatedFields(
    title = models.CharField(max_length=200),
    desc = models.TextField()
    )
    pic = models.ImageField(upload_to='Team')
    
