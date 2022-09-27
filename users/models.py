from datetime import date

from django.db import models


# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    email = models.EmailField(max_length=50, null=True, unique=True)
    password = models.CharField(max_length=50, null=True)
    birth_date = models.DateField(null=True)

    def age(self):
        today = date.today()
        age = today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return age

    def __str__(self):
        return f"{self.full_name} - {self.age} - {self.email}"

    class Meta:
        db_table = "User"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = [
            'first_name',
            'last_name'
        ]
       