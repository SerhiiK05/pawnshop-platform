# Generated by Django 4.1 on 2024-12-02 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pawnshop", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="referralbonus",
            options={
                "verbose_name": "referral-bonus",
                "verbose_name_plural": "referral-bonuses",
            },
        ),
        migrations.AlterField(
            model_name="referralbonus",
            name="bonus_amount",
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="balance",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
