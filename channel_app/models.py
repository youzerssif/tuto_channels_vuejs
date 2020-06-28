from django.db import models
# User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Create your models here.


########################################## U T I L I S A T E U R ###########################################

class Utilisateur(models.Model):
    """Model definition for Utilisateur."""

    # TODO: Define fields here
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='utilisateur')
    photo = models.ImageField(upload_to='photo_utilisateur', default="profileimage.png", null = True, blank = True)
    

    statut = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_upd = models.DateTimeField(auto_now=True)
    
    class Meta:
        """Meta definition for Utilisateur."""

        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        """Unicode representation of Utilisateur."""
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Utilisateur.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, created, **kwargs):
            
        instance.utilisateur.save()

class Chat(models.Model):
    """Model definition for Chat."""

    # TODO: Define fields here
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatuser',blank=True, null=True)
    message = models.TextField()

    statut = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_upd = models.DateTimeField(auto_now=True)


    class Meta:
        """Meta definition for Chat."""

        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'

    def __str__(self):
        """Unicode representation of Chat."""
        return self.user.username

    def last_10_messages():
        return Chat.objects.order_by('-date_add').all()[:10]