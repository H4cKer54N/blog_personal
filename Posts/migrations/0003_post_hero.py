# Generated by Django 5.0.3 on 2024-03-14 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0002_post_trending_alter_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='hero',
            field=models.BooleanField(default=False),
        ),
    ]
