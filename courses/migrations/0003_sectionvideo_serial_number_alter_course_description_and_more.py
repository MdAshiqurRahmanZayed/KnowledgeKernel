# Generated by Django 4.1.3 on 2022-12-15 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0002_course_instructor"),
    ]

    operations = [
        migrations.AddField(
            model_name="sectionvideo",
            name="serial_number",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="course",
            name="description",
            field=models.CharField(max_length=700, null=True),
        ),
        migrations.AlterField(
            model_name="course",
            name="length",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="course",
            name="prerequisite",
            field=models.CharField(
                blank=True, default="No need ", max_length=50, null=True
            ),
        ),
        migrations.AlterField(
            model_name="course",
            name="price",
            field=models.IntegerField(default=0),
        ),
    ]
