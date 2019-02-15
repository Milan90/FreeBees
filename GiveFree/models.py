from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class Institution(models.Model):
    name = models.CharField(max_length=250)
    goal = models.CharField(max_length=200)
    groups = models.ManyToManyField("Groups")
    address = models.OneToOneField("InstitutionAddress", on_delete=models.CASCADE)


class Groups(models.Model):
    name = models.CharField(max_length=100)


class InstitutionAddress(models.Model):
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    building_number = models.SmallIntegerField(validators=[MinValueValidator(1)])
    flat_number = models.SmallIntegerField(null=True)
    zip_code = models.CharField(max_length=6)


class PickupAddress(models.Model):
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=6)
    pickup_date = models.DateField()
    pickup_time = models.TimeField()
    comments = models.TextField(null=True)


class Gifts(models.Model):
    gifts_kind = models.TextField()
    bags_amount = models.SmallIntegerField()
    from_who = models.ForeignKey(User, on_delete=models.CASCADE)
    institution = models.OneToOneField(Institution, on_delete=models.CASCADE)
    creation_date = models.DateField(auto_now_add=True)
    delivery_address = models.OneToOneField(PickupAddress, on_delete=models.CASCADE)
    is_delivered = models.BooleanField(default=False)
    delivery_date = models.DateField(null=True)


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=250)
    message = models.TextField()
