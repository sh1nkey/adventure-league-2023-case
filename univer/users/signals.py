from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, StudentProfile, BaseProfile, TeacherProfile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        role_mapping = {
            1: BaseProfile.objects.create,
            2: StudentProfile.objects.create,
            3: TeacherProfile.objects.create,
            4: BaseProfile.objects.create,
        }

        profile_creator = role_mapping.get(instance.role)
        if profile_creator:
            profile_creator(user=instance)
        else:
            print("smth went wrong")
