# Generated by Django 3.2.9 on 2023-04-23 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20230423_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='courses', to='courses.Category'),
        ),
    ]
