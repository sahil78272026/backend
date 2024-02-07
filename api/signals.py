from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *

# if a SingalTable object is created,  post_save signal will be fired
@receiver(post_save, sender=SingalTable)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print("singal executed")
        # Perform any operations.

# if a User is updated, NewUser instance will also be updated.
# newuser is used for reverse relationship from User model to newuser model.
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.newuser.save()