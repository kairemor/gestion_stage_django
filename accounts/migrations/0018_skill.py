# Generated by Django 2.2.2 on 2019-07-10 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_auto_20190705_1720'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('students', models.ManyToManyField(related_name='my_skills', to='accounts.Student')),
            ],
        ),
    ]