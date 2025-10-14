from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from datetime import datetime
import os


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    trainer_for = models.CharField(max_length=100, verbose_name="Træner for")
    reg_number = models.CharField(max_length=50, verbose_name="Reg nr")
    account_number = models.CharField(max_length=50, verbose_name="Konto nr")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        if hasattr(instance, 'profile'):
            instance.profile.save()


class Kursus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kursus_records')
    kursus = models.CharField(max_length=200, verbose_name="Kursus")
    sted = models.CharField(max_length=100, verbose_name="Sted")
    arrangor = models.CharField(max_length=100, verbose_name="Arrangør")
    pris = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Pris")
    date = models.DateField(verbose_name="Dato")
    bilagsnr = models.CharField(max_length=50, verbose_name="Bilagsnr", unique=True, editable=False)
    
    # File storage as blob in database
    file_data = models.BinaryField(verbose_name="Fil Data", null=True, blank=True)
    file_name = models.CharField(max_length=255, verbose_name="Fil Navn", null=True, blank=True)
    file_size = models.PositiveIntegerField(verbose_name="Fil Størrelse", null=True, blank=True)
    file_type = models.CharField(max_length=100, verbose_name="Fil Type", null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Kursus"
        verbose_name_plural = "Kursus Records"
        ordering = ['-created_at']

    def generate_bilagsnr(self):
        """Generate a unique bilagsnr"""
        # Format: YYYYMMDD-XXXX (date + 4 random digits)
        date_str = datetime.now().strftime('%Y%m%d')
        random_suffix = str(uuid.uuid4().hex[:4]).upper()
        return f"{date_str}-{random_suffix}"
    
    def save(self, *args, **kwargs):
        if not self.bilagsnr:
            self.bilagsnr = self.generate_bilagsnr()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.kursus} - {self.sted} ({self.user.username})"

    @property
    def filename(self):
        """Get the filename from the stored file data"""
        return self.file_name
    
    @property
    def has_file(self):
        """Check if the kursus has an attached file"""
        return self.file_data is not None and len(self.file_data) > 0
