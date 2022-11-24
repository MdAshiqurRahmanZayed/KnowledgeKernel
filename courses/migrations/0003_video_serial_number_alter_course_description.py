# Generated by Django 4.1.3 on 2022-11-22 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0002_video"),
    ]

    operations = [
        migrations.AddField(
            model_name="video",
            name="serial_number",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="course",
            name="description",
            field=models.CharField(max_length=500, null=True),
        ),
    ]
