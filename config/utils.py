
import requests
# from django.core.mail import EmailMultiAlternatives
# from django.dispatch import receiver
# from django.template.loader import render_to_string
# from django.urls import reverse
# from django_rest_passwordreset.signals import reset_password_token_created
# from django.core.mail import send_mail 

# @receiver(reset_password_token_created)
# def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
#     """
#     Handles password reset tokens
#     When a token is created, an e-mail needs to be sent to the user
#     :param sender: View Class that sent the signal
#     :param instance: View Instance that sent the signal
#     :param reset_password_token: Token Model Object
#     :param args:
#     :param kwargs:
#     :return:
#     """
#     # send an e-mail to the user
#     context = {
#         'current_user': reset_password_token.user,
#         'username': reset_password_token.user.username,
#         'email': reset_password_token.user.email,
#         'reset_password_url': "{}?token={}".format(
#             instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
#             reset_password_token.key)
#     }

#     # render email text
#     email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

#     send_mail(
#         # title:
#         "Password Reset for {title}".format(title="N9dar"),
#         # message:
#         email_plaintext_message,
#         # from:
#         "support@n9dar.com",
#         # to:
#         [reset_password_token.user.email]
#     )

def verify_recaptcha(response):
    data = {
        'secret': 'YOUR_SECRET_KEY',
        'response': response,
    }
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    if response.status_code == 200 and response.json().get('success'):
        return True
    else:
        return False

def get_image_upload_to(instance, filename):
    return f"{instance.__class__.__name__.lower()}/{instance.pk}/images/{filename}"

def get_cover_upload_to(instance, filename):
    return f"{instance.__class__.__name__.lower()}/{instance.pk}/covers/{filename}"