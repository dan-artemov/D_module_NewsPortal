# Generated by Django 4.2.1 on 2023-06-03 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_alter_category_subscribers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='subscribers',
        ),
    ]
