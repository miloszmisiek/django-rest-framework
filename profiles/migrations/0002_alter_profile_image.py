# Generated by Django 3.2.14 on 2022-07-21 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='../default_profile_ymgggi', upload_to='images/'),
        ),
    ]
