# Generated by Django 5.0.4 on 2024-05-18 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_readingprocess_last_update_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='readerinfo',
            name='default_narrator',
            field=models.IntegerField(default=0),
        ),
    ]