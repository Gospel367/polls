# Generated by Django 4.0.2 on 2022-07-01 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls_app', '0006_alter_profile_email_confirmed_alter_profile_fullname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='fullname',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
