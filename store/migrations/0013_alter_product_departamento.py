# Generated by Django 4.1.5 on 2023-01-12 23:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0008_department_alter_userprofile_departamento'),
        ('store', '0012_alter_product_departamento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='departamento',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='userprofile.department'),
        ),
    ]
