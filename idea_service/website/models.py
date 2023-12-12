from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse


class Pins(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField(max_length=255, blank=True)
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    collection = models.ForeignKey('Collections', on_delete=models.CASCADE, null=True)
    video = models.FileField(upload_to='videos/%Y/%m/%d/', null=True, blank=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d/', null=True, blank=True)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('pin', kwargs={'pin_id': self.pk})


class Collections(models.Model):
    title = models.CharField(max_length=18)
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    collection_image = models.ImageField(upload_to='collections/')

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('collection', kwargs={'collection_id': self.pk})


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users/', null=True)
    email = models.EmailField(unique=True, null=True)
    about = models.TextField(max_length=255, null=True)

    def __str__(self):
        return f'{self.user.username}'

    def get_absolute_url(self):
        return reverse('profile', kwargs={'profile_id': self.pk})


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance, photo='users/default-profile-photo.jpg')
        Collections.objects.create(title='Избранное',
                                   author=profile,
                                   collection_image='collections/favorites.jpg')


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
