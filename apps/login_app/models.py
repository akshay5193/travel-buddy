from __future__ import unicode_literals
from django.db import models
from django.contrib import messages


class UserManager(models.Manager):
    def basic_validator_register(self, postData):
        errors = {}
        if len(postData['input_first_name']) < 2:
            errors["valid_first_name"] = "First name should be at least 2 characters"
        if len(postData['input_last_name']) < 2:
            errors["valid_last_name"] = "Last name should be at least 2 characters"
        if '@' not in postData['input_email']:
            errors["valid_email"] = "Email address should include @ sign"
        if len(postData['input_password']) < 8:
            errors["valid_password_length"] = "Password should be at least 8 characters"
        if postData['input_password'] != postData['input_confirm_password']:
            errors["valid_password_match"] = "Password should match with Confirm PW"
        return errors

    def basic_validator_login(self, postData):
        errors = {}
        if '@' not in postData['input_email']:
            errors["valid_email"] = "Email address should include @ sign"
        if len(postData['input_password']) < 8:
            errors["valid_password_length"] = "Password should be at least 8 characters"
        return errors


class TripManager(models.Manager):
    def basic_validator_trip(self, postData):
        errors = {}

        if len(postData['input_destination']) < 1:
            errors["valid_destination"] = "A destination must be provided!"
        elif len(postData['input_destination']) < 3:
            errors["valid_destination"] = "A destination must consist of at least 3 characters!"

        if len(postData['input_start_date']) < 1:
            errors["valid_start_date"] = "A start date must be provided!"

        if len(postData['input_end_date']) < 1:
            errors["valid_end_date"] = "An end date must be provided!"

        if len(postData['input_plan']) < 1:
            errors["valid_plan"] = "A plan must be provided!"
        elif len(postData['input_plan']) < 3:
            errors["valid_plan"] = "A plan must consist of at least 3 characters!"

        if postData['input_start_date'] > postData['input_end_date']:
            errors["valid_date"] = "You cannot travel back in time!"

        if postData['input_start_date'] < postData['date_rn']:
            errors["valid_date"] = "You cannot make a trip back in time!"

        if postData['input_end_date'] < postData['input_start_date']:
            errors["valid_date"] = "Please select an end date which is on or after the start date!"

        return errors


class Trip(models.Model):
    destination = models.CharField(max_length=45)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    created_by = models.CharField(max_length=45)
    updated_at = models.DateField(auto_now_add=True)
    objects = TripManager()


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    trip = models.ManyToManyField(Trip, related_name="user_trip")
    objects = UserManager()
