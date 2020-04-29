import uuid
import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **args):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **args)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Classroom(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    time = models.DateTimeField()
    students = models.ManyToManyField('student')
    grades = models.ManyToManyField('grade')

    def __str__(self):
        return self.name


class Grade(models.Model):
    letter_grade = models.CharField(max_length=5)
    value = models.IntegerField()
    value_received = models.IntegerField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    percentage_of_final_grade = models.IntegerField()

    def __str__(self):
        return self.name


class Student(models.Model):
    YEAR_IN_SCHOOL_CHOICES = [
        (0, 'K'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
        (11, '11'),
        (12, '12'),
    ]
    GENDER = [
        (0, 'Male'),
        (1, 'Female'),
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    grade_level = models.IntegerField(
        choices=YEAR_IN_SCHOOL_CHOICES,
    )
    age = models.IntegerField()
    gender = models.IntegerField(
        choices=GENDER,
    )
    disability = models.BooleanField(default=False)
    grade = models.ManyToManyField('grade')

    def __str__(self):
        return self.name
