from django.db import models


# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=50, null=True, unique=True)
    description = models.TextField(max_length=1000, null=True)

    def __str__(self):
        return f"{self.name}'s description is : {self.description}"

    class Meta:
        db_table = "Courses"
        verbose_name = "Course"
        ordering = [
            'name'
        ]
