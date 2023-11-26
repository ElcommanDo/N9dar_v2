# Generated by Django 3.2.9 on 2023-11-25 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teammember',
            name='desc',
        ),
        migrations.RemoveField(
            model_name='teammember',
            name='title',
        ),
        migrations.AddField(
            model_name='customuser',
            name='country',
            field=models.CharField(default='ss', max_length=220),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='full_name',
            field=models.CharField(default='ss', max_length=220),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('N', 'Prefer not to say')], default='N', max_length=1),
        ),
        migrations.AddField(
            model_name='customuser',
            name='mobile',
            field=models.CharField(default='ss', max_length=50),
            preserve_default=False,
        ),
    ]