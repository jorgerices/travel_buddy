from django.contrib.messages.api import error
from django.db import models
from datetime import datetime
import re
from django.core.validators import MaxValueValidator, MinValueValidator

class UserManager(models.Manager):
    def validador_basico(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        SOLO_LETRAS = re.compile(r'^[a-zA-Z. ]+$')

        errors = {}

        if len(postData['name']) < 3:
            errors['name_len'] = "El nombre de usuario debe tener al menos 3 caracteres"

        if len(postData['firstname']) < 3:
            errors['firstname_len'] = "El nombre debe tener al menos 3 caracteres"

        if len(postData['lastname']) < 3:
            errors['lastname_len'] = "El apellido debe tener al menos 3 caracteres"

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Ingrese un email válido"

        if not SOLO_LETRAS.match(postData['firstname']):
            errors['solo_letras'] = "Ingrese solo letras en el campo 'Nombre'"

        if not SOLO_LETRAS.match(postData['lastname']):
            errors['solo_letras'] = "Ingrese solo letras en el campo 'Apellido'"

        if len(postData['password']) < 8:
            errors['password'] = "La contraseña debe tener al menos 8 caracteres"

        if postData['password'] != postData['password_confirm'] :
            errors['password_confirm'] = "contraseña y confirmar contraseña no son iguales"

        return errors

class TripManager(models.Manager):
    def trip_validator(self, postData):
        errors = {}
        print(postData['start_date'])
        print(postData['end_date'])
        
        if postData['start_date'] == '':
            errors['empty_start'] = "Debes ingresar una fecha de inicio"
        if postData['end_date'] == '':
            errors['empty_end'] = "Debes ingresar una fecha de finalización"
        
        if postData['end_date'] != '' and postData['start_date']!= '':
            present= datetime.now()
            start = datetime.strptime(postData['start_date'], '%Y-%m-%d')
            end = datetime.strptime(postData['end_date'], '%Y-%m-%d')
            if start < present:
                errors['startdate']= "La fecha de inicio no puede ser previa a la de fecha de hoy"
            elif end < start:
                errors['enddate']= "La fecha de inicio no puede ser posterior a la de fecha de finalización"
        return errors

class User(models.Model):
    CHOICES = (
        ("user", 'User'),
        ("admin", 'Admin')
    )
    name = models.CharField(max_length=100, unique=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    role = models.CharField(max_length=255, choices=CHOICES)
    password = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"

class Trip(models.Model):
    destination = models.CharField(max_length=255, unique=True)
    start_date = models.DateField(auto_now=False)
    end_date = models.DateField(auto_now=False)
    plan = models.TextField()
    creator = models.ForeignKey(User, related_name='my_trips', on_delete=models.CASCADE)
    travellers = models.ManyToManyField(User, related_name='trips')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects =TripManager()
  
    def __str__(self):
        return f"{self.destination}"

    def __repr__(self):
        return f"{self.destination}"