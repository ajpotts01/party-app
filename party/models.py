# Standard lib imports
import uuid

# Third-party imports
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    pass


class Party(models.Model):
    uuid: models.UUIDField = models.UUIDField(primary_key=True, default=uuid.uuid4)
    party_date: models.DateField = models.DateField()
    party_time: models.TimeField = models.TimeField()
    invitation: models.CharField = models.CharField(max_length=200)
    venue: models.CharField = models.CharField(max_length=200)
    organizer: models.ForeignKey = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organized_parties",
    )

    class Meta:
        verbose_name_plural: str = "parties"

    def __str__(self) -> str:
        return f"{self.venue}, {self.party_date}"


class Gift(models.Model):
    uuid: models.UUIDField = models.UUIDField(primary_key=True, default=uuid.uuid4)
    gift: models.CharField = models.CharField(max_length=200)
    price: models.FloatField = models.FloatField(blank=True, null=True)  # Decimal?
    link: models.URLField = models.URLField(max_length=200, blank=True, null=True)
    party: models.ForeignKey = models.ForeignKey(to=Party, on_delete=models.CASCADE)

    def __str__(self):
        return self.gift


class Guest(models.Model):
    uuid: models.UUIDField = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name: models.CharField = models.CharField(max_length=200)
    attending: models.BooleanField = models.BooleanField(default=False)
    party: models.ForeignKey = models.ForeignKey(
        to=Party, on_delete=models.CASCADE, related_name="guests"
    )

    def __str__(self):
        return str(self.name)
