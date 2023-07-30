# Generated by Django 3.2.9 on 2023-04-23 13:04

import config.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_At', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('code', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=config.utils.get_image_upload_to)),
                ('cover', models.ImageField(blank=True, null=True, upload_to=config.utils.get_cover_upload_to)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField()),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('course_type', models.CharField(choices=[('Free', 'Free'), ('Paid', 'Paid')], default='Free', max_length=4)),
                ('is_online', models.BooleanField(default=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('instructor', models.ForeignKey(limit_choices_to={'groups__name': 'Instructor'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
    ]
