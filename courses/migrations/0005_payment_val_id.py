# Generated by Django 4.1.3 on 2023-03-10 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0004_payment"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="val_id",
            field=models.CharField(default=1, max_length=60),
            preserve_default=False,
        ),
    ]
