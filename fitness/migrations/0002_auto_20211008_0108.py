# Generated by Django 3.2.6 on 2021-10-07 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='events',
            name='amount',
        ),
        migrations.AddField(
            model_name='events',
            name='price',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
