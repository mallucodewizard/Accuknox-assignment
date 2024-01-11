# Generated by Django 4.1.3 on 2024-01-11 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0002_user_login_type_alter_user_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='login_type',
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]