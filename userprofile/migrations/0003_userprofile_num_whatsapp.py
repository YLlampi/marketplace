# Generated by Django 4.1.5 on 2023-01-10 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_userprofile_is_vendor'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='num_whatsapp',
            field=models.CharField(max_length=9, null=True),
        ),
    ]