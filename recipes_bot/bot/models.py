from django.db import models


class User(models.Model):
    CHOICES = [('Male', 'Чоловіча'), ('Female', 'Жіноча')]
    # додати імена полів
    user_id = models.IntegerField(primary_key=True)  # message.from_user.id
    first_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64, null=True)
    username = models.CharField(max_length=64, null=True)
    name = models.CharField(max_length=50, null=True)
    gender = models.CharField(max_length=6, null=True)
    state = models.CharField(max_length=32, null=True)

    def __str__(self):
        return f'<User> {self.name}'


class Recipe(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    photo = models.ImageField(null=True, blank=True, upload_to='images/')