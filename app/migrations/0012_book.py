# Generated by Django 5.0.4 on 2024-05-09 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_reader'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('genre', models.CharField(max_length=50)),
                ('rating', models.FloatField()),
                ('summary', models.TextField()),
                ('total_pages', models.PositiveIntegerField()),
                ('image_url', models.URLField()),
                ('book_url', models.URLField()),
                ('original_font_size', models.PositiveIntegerField()),
            ],
        ),
    ]
