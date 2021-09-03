from django.db import models
import re
from datetime import datetime, timedelta
from calendar import isleap
# Create your models here.
class UserManager(models.Manager):
    def validador_basico(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        SOLO_LETRAS = re.compile(r'^[a-zA-Z. ]+$')
        
        lista =[]
        # for c in User.objects.all():
        #     lista.append(c.email)
        #     print(c.email)
            
        errors = {}
        # if postData['email'] in lista:
        #     errors['email-unico'] = "el email ya existe"
        if User.objects.filter(email = postData['email']).exists():
            errors['email-unico'] = "el email ya existe"
        # Revisando el primer nombre
        if len(postData['name']) == 0:
            errors['first_name_emp'] = "No se permite Nombre vacio"
        elif len(postData['name']) > 0 and len(postData['name']) < 2:
            errors['show_title_len'] = "Su Nombre debe contener almenos dos caracteres"
            
        # checking alias
        if len(postData['alias']) == 0:
            errors['last_name_emp'] = "No se permite el apellido Vacio"
        elif len(postData['alias']) > 0 and len(postData['alias']) < 2:
            errors['last_name_len'] = "Su apellido debe contener al menos dos caracteres"

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "correo invalido"

        if not SOLO_LETRAS.match(postData['name']):
            errors['solo_letras'] = "solo letras en nombre por favor"

        if len(postData['birthday']) == 0:
            errors['birthday_emp'] = "Birthday can not be empty"      
        else:
            # The strptime() method creates a datetime object from the given string.            
            birthday_date = datetime.strptime(postData['birthday'], "%Y-%m-%d")
            today_date = datetime.today()

            yesterday = today_date - timedelta(days=1)
                
            start_date = birthday_date
            end_date = today_date
            diffyears = end_date.year - start_date.year
            difference  = end_date - start_date.replace(end_date.year)
            days_in_year = isleap(end_date.year) and 366 or 365
            difference_in_years = diffyears + (difference.days + difference.seconds/86400.0)/days_in_year              
            
            # If user is less than 16 years old
            if difference_in_years < 16:
                errors['birthday_old'] = "La edad debe ser al menos 16 años para registrarse"   

        if len(postData['password']) < 4:
            errors['password'] = "contraseña debe tener al menos 8 caracteres";

        if postData['password'] != postData['password2'] :
            errors['password_confirm'] = "contraseña y confirmar contraseña no son iguales. "

        
        return errors


class User(models.Model):

    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    birthday = models.DateField(default=datetime.now)
    password = models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    #users = lista de usuarios amigos, inversa
    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"

class Friend(models.Model):
    user_friend = models.ForeignKey(User, related_name='requester',on_delete=models.CASCADE)
    second_friend = models.ForeignKey(User, related_name='accepter',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)