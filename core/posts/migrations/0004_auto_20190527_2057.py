# Generated by Django 2.1.8 on 2019-05-27 20:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='product',
            new_name='post',
        ),
    ]
