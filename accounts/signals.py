from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
import uuid
from .models import AdminProfile, PartnerProfile, StudentProfile, InstructorProfile


User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        confirmation_code = str(uuid.uuid4())
        instance.confirmation_code = confirmation_code
        instance.is_active = True
        

        # subject = 'Confirm your account'
        # message = f'Hi {instance.username},\n\nPlease click on the link below to confirm your account:\n\n{settings.BASE_URL}/confirm/?confirmation_code={instance.confirmation_code}\n\nThanks for signing up!'
        # from_email = settings.DEFAULT_FROM_EMAIL
        # recipient_list = [instance.email]
        # try:
        #     send_mail(subject, message, from_email, recipient_list)
        # except:
        #     pass

        if instance.role == 'admin':
            AdminProfile.objects.create(user=instance)
        
        elif instance.role == 'student':
            StudentProfile.objects.create(user=instance)
        
        elif instance.role == 'partner':
            PartnerProfile.objects.create(user=instance)
        
        elif instance.role == 'instructor':
            InstructorProfile.objects.create(user=instance)
        instance.save()
        
        
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.role == 'admin':
        instance.admin_profile.save()
    
    elif instance.role == 'student':
        instance.student_profile.save()
    
    elif instance.role == 'instructor':
        instance.instructor_profile.save()
    
    elif instance.role == 'partner':
        instance.partner_profile.save()
