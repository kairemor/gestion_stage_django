# Generated by Django 2.2.2 on 2019-06-28 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20190628_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='framer',
            name='status',
            field=models.CharField(default='framer', max_length=50),
        ),
        migrations.AlterField(
            model_name='student',
            name='classe',
            field=models.CharField(choices=[('TC2', 'Tronc Commun 2'), ('DIC1', "Diplome d'Ingenieur de Conception 1"), ('DIC2', "Diplome d'Ingenieur de Conception 2"), ('DIC3', "Diplome d'Ingenieur de Conception 3")], max_length=50),
        ),
        migrations.AlterField(
            model_name='student',
            name='department',
            field=models.CharField(choices=[('GIT', 'Genie Informatique et Telecommunication'), ('GEM', 'Genie ElectroMecanique '), ('GC', 'Genie Civil')], max_length=50),
        ),
        migrations.AlterField(
            model_name='student',
            name='status',
            field=models.CharField(default='student', max_length=50),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='status',
            field=models.CharField(default='teacher', max_length=50),
        ),
    ]
