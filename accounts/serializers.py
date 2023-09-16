from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth import password_validation
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import authenticate
from .models import *
from config.utils import verify_recaptcha
from parler_rest.serializers import TranslatableModelSerializer
from config.mixin import TranslatedSerializerMixin 
from parler_rest.fields import TranslatedFieldsField


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user'] = CustomUserSerializer(self.user).data
        return data



class UserRegisterationSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize registration requests and create a new user.
    """
    password2 = serializers.CharField(write_only=True, required=True)
    #captcha = serializers.CharField()
    class Meta:
        model = CustomUser
        fields = ("id", "username","full_name", "email","role", "password", "password2") 
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        if CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email already exist."})
        
        return attrs
    
    # def validate_captcha(self, value):
    #     if not verify_recaptcha(value):
    #         raise serializers.ValidationError('reCAPTCHA verification failed')
    #     return value
        
    

    def create(self, validated_data):
        validated_data.pop('password2')
        return CustomUser.objects.create_user(**validated_data)
    

class UserLoginSerializer(serializers.Serializer):
    """
    Serializer class to authenticate users with email and password.
    """

    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')



class ChangePasswordSerializer(serializers.Serializer):
    model = CustomUser

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        # Validate the new password using Django's password validation rules
        password_validation.validate_password(value)
        return value
    
    def create(self, validated_data):
        # Get the user from the context and create a password change form
        user = self.context['request'].user
        form = SetPasswordForm(user=user, data=validated_data)

        # Save the new password and return the user instance
        if form.is_valid():
            form.save()
            return user
        else:
            raise serializers.ValidationError(form.errors)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True


class AdminProfileSerializer(ProfileSerializer):
    class Meta:
        model = AdminProfile
        fields = ['date_of_hire', 'job_title']


class StudentProfileSerializer(ProfileSerializer):
    class Meta:
        model = StudentProfile
        fields = ['major', 'gpa']


class InstructorProfileSerializer(ProfileSerializer):
    class Meta:
        model = InstructorProfile
        fields = ['department', 'teaching_experience']


class PartnerProfileSerializer(ProfileSerializer):
    class Meta:
        model = PartnerProfile
        fields = []


class CustomUserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'email','username', 'first_name', 'last_name','confirmation_code', 'is_active', 'is_staff', 'role', 'profile']
        read_only_fields = ('id', 'is_active', 'is_staff')


    def get_profile(self, obj):
        if obj.role == 'admin':
            serializer = AdminProfileSerializer(obj.admin_profile)
        
        elif obj.role == 'student':
            serializer = StudentProfileSerializer(obj.student_profile)
        
        elif obj.role == 'instructor':
            serializer = InstructorProfileSerializer(obj.instructor_profile)
        
        elif obj.role == 'partner':
            serializer = InstructorProfileSerializer(obj.partner_profile)
        
        else:
            serializer = ProfileSerializer()
        return serializer.data
    
    def update(self, instance, validated_data):
        role = validated_data.pop('role', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if role:
            if role == 'admin':
                if hasattr(instance, 'student_profile'):
                    instance.student_profile.delete()
                if hasattr(instance, 'instructor_profile'):
                    instance.instructor_profile.delete()
                if hasattr(instance, 'partner_profile'):
                    instance.partner_profile.delete()
                if not hasattr(instance, 'admin_profile'):
                    AdminProfile.objects.create(user=instance)
            
            elif role == 'student':
                if hasattr(instance, 'admin_profile'):
                    instance.admin_profile.delete()
                if hasattr(instance, 'instructor_profile'):
                    instance.instructor_profile.delete()
                if hasattr(instance, 'partner_profile'):
                    instance.partner_profile.delete()
                if not hasattr(instance, 'student_profile'):
                    StudentProfile.objects.create(user=instance)
            
            elif role == 'instructor':
                if hasattr(instance, 'admin_profile'):
                    instance.admin_profile.delete()
                if hasattr(instance, 'student_profile'):
                    instance.student_profile.delete()
                if hasattr(instance, 'partner_profile'):
                    instance.partner_profile.delete()
                if not hasattr(instance, 'instructor_profile'):
                    InstructorProfile.objects.create(user=instance)
            
            elif role == 'partner':
                if hasattr(instance, 'admin_profile'):
                    instance.admin_profile.delete()
                if hasattr(instance, 'student_profile'):
                    instance.student_profile.delete()
                if hasattr(instance, 'instructor_profile'):
                    instance.instructor_profile.delete()
                if not hasattr(instance, 'partner_profile'):
                    PartnerProfile.objects.create(user=instance)

        if hasattr(instance, 'admin_profile') and 'admin_profile' in validated_data:
            admin_profile_data = validated_data.pop('admin_profile')
            admin_profile_serializer = AdminProfileSerializer(instance=instance.admin_profile, data=admin_profile_data, partial=True)
            if admin_profile_serializer.is_valid():
                admin_profile_serializer.save()

        if hasattr(instance, 'student_profile') and 'student_profile' in validated_data:
            student_profile_data = validated_data.pop('student_profile')
            student_profile_serializer = StudentProfileSerializer(instance=instance.student_profile, data=student_profile_data, partial=True)
            if student_profile_serializer.is_valid():
                student_profile_serializer.save()

        if hasattr(instance, 'instructor_profile') and 'instructor_profile' in validated_data:
            instructor_profile_data = validated_data.pop('instructor_profile')
            instructor_profile_serializer = InstructorProfileSerializer(instance=instance.instructor_profile, data=instructor_profile_data, partial=True)
            if instructor_profile_serializer.is_valid():
                instructor_profile_serializer.save()

        if hasattr(instance, 'partner_profile') and 'partner_profile' in validated_data:
            partner_profile_data = validated_data.pop('partner_profile')
            partner_profile_serializer = PartnerProfileSerializer(instance=instance.partner_profile, data=partner_profile_data, partial=True)
            if partner_profile_serializer.is_valid():
                partner_profile_serializer.save()

        instance.save()
        return instance
    

class TeamMemeberSerializer(TranslatedSerializerMixin, TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=TeamMember, read_only=True)
    class Meta:
        model = TeamMember
        fields = ['id', 'translations', 'pic']

