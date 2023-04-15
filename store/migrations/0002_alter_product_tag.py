# Generated by Django 3.2.5 on 2023-03-22 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='tag',
            field=models.CharField(blank=True, choices=[('skincare', 'Fiction'), ('makeup', 'Non-Fiction'), ('bath&body', 'Study')], default='skincare', max_length=100, null=True),
        ),
    ]
