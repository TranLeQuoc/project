# Generated by Django 5.0.4 on 2024-05-17 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_alter_book_original_font_size_alter_book_rating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readingprocess',
            name='book_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='readingprocess',
            name='user_id',
            field=models.IntegerField(),
        ),
    ]
