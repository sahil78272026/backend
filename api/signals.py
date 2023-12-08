from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *

# if a User object is created,  post_save signal will be fired and a NewUser will also be created.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        NewUser.objects.create(user=instance)

# if a User is updated, NewUser instance will also be updated.
# newuser is used for reverse relationship from User model to newuser model.
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.newuser.save()