# Generated by Django 4.0.2 on 2022-07-05 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls_app', '0008_delete_choice_delete_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='image',
            field=models.ImageField(blank=True, upload_to='media/'),
        ),
    ]
