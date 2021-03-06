# Generated by Django 2.2.2 on 2019-06-26 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0001_initial'),
        ('accounts', '0003_auto_20190626_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='framer',
            name='enterprise',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='framers', to='internship.Enterprise'),
        ),
        migrations.AddField(
            model_name='student',
            name='enterprise',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='internship.Enterprise'),
        ),
    ]
