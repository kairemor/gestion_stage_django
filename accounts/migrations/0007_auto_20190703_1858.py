# Generated by Django 2.2.2 on 2019-07-03 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20190628_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='framer',
            name='image',
            field=models.ImageField(null=True, upload_to='profiles/'),
        ),
        migrations.AddField(
            model_name='student',
            name='image',
            field=models.ImageField(null=True, upload_to='profiles/'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='image',
            field=models.ImageField(null=True, upload_to='profiles/'),
        ),
    ]
