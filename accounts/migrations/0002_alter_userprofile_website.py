# Generated by Django 4.1.3 on 2023-03-08 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="website",
            field=models.CharField(max_length=70),
        ),
    ]