# Generated by Django 4.1.1 on 2022-09-27 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('description', models.TextField(max_length=1000, null=True)),
            ],
            options={
                'verbose_name': 'Course',
                'db_table': 'Courses',
                'ordering': ['name'],
            },
        ),
    ]
