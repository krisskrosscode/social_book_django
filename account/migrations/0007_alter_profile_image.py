# Generated by Django 4.0.3 on 2023-02-27 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='profile_pictures/default.png', upload_to='profile_pictures/<django.db.models.query_utils.DeferredAttribute object at 0x00000295D6E41730>/'),
        ),
    ]
