# Generated by Django 4.1.5 on 2023-01-15 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_alter_product_departamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_new',
            field=models.BooleanField(default=True, null=True, verbose_name='Es nuevo?'),
        ),
    ]