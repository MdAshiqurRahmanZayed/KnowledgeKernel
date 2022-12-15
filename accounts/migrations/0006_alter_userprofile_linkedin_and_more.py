# Generated by Django 4.1.3 on 2022-12-15 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0005_rename_linkdin_userprofile_linkedin"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="linkedin",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="profile_picture",
            field=models.ImageField(
                blank=True,
                default="images/man.png",
                null=True,
                upload_to="images/profile",
            ),
        ),
    ]