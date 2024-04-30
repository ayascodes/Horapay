from django.core.mail import send_mail
from django.conf import settings
import random

from django.template.loader import render_to_string

from .models import CustomUser
from django.urls import reverse


def send_activation_email(email,password):
    subject="Votre compte HoraPay"
    login_url=f"http://127.0.0.1:8000/testing/token/"
    message = f"Bonjour,\n\nVotre compte HoraPay a été créé avec succès. Voici vos informations de connexion :\n\nEmail: {email}\nMot de passe: {password}\n\nVous pouvez vous connecter à votre compte en utilisant le lien suivant :\n{login_url}\n\nCordialement,\nL'équipe HoraPay"
    email_from = settings.EMAIL_HOST
    send_mail(subject,message,email_from,[email])
    user_obj = CustomUser.objects.get(email=email)
    user_obj.save()

def send_reset_password_email(email,reset_token):
    subject="Reintialiser votre mot de passe sur HoraPay"
    reset_link = f"http://127.0.0.1:8000/testing/reset-password/{reset_token}/"
    message =f"Bonjour,\n\nVous pouvez re-intialiser votre mot de passe ici. Voici votre lien d'intialisation :{reset_link}\n\nCordialement,\nL'équipe HoraPay"
    email_from = settings.EMAIL_HOST
    send_mail(subject,message,email_from,[email])
    user_obj = CustomUser.objects.get(email=email)
    user_obj.save()