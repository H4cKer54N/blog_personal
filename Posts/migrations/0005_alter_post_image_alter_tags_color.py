# Generated by Django 5.0.3 on 2024-03-15 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0004_contactform'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='post_images'),
        ),
        migrations.AlterField(
            model_name='tags',
            name='color',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
