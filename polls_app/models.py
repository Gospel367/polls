from django.db import models
import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify


class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, related_name='saver')
    fullname =models.CharField(max_length=200, blank=True, null=True)
    phone =models.IntegerField(default=0)
    state =models.CharField(max_length=200)
    country =models.CharField(max_length=200)
    email_confirmed = models.BooleanField(default=True)
    
    def __str__(self):
        return self.username.first_name
    
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(username=instance, email_confirmed=False)
        instance.saver.save()
        
        
class Newsletter(models.Model):
    title = models.CharField(max_length=100, null=True)
    slug =models.SlugField(max_length=100)
    author =  models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)
    post_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='media/', blank=True)
    link = models.URLField(max_length=200)
    country = models.CharField(max_length=100, null=True)

    class Meta:
        ordering = ['post_date']
        verbose_name = 'newsletter'
        verbose_name_plural = 'newsletters'
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Newsletter, self).save(*args, **kwargs)
        