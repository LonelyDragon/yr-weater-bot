from django.db import models
from django.db.models.fields.related import ForeignKey

# Create your models here.

class Users(models.Model):
    user_id = models.AutoField(
        primary_key=True, auto_created=True, 
        unique=True, editable=False,
        help_text="unique id user")
    user_id_telegram = models.IntegerField(
        max_length=25,
        help_text="user's telegram unique id")
    username = models.CharField(
        max_length=255, editable=False,
        help_text="unique user's login Telegram")
    first_name = models.CharField(
        max_length=255, editable=False,
        blank=True)
    last_name = models.CharField(
        max_length=255, editable=False,
        blank=True)
    language_code = models.CharField(
        max_length=10, help_text="IETF BCP 47 language tag")
    last_active = models.DateField(
        help_text="last user's active")


class UserSettings(models.Model):

    user_id = models.ForeignKey(
        Users, on_delete=models.CASCADE)    
    lat = models.FloatField(
        max_lenght=20, help_text="latitude",
        blank=False)
    lon = models.FloatField(
        max_lenght=20, help_text="longitude",
        blank=False)
    altitude = models.IntegerField(
        max_length=6, help_text="Whole meters above sea level",
        blank=True
    )
    time_send = models.TimeField(
        help_text="time, when we send weather")

