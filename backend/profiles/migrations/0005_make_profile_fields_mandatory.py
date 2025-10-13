# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_alter_kursus_file_optional'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='trainer_for',
            field=models.CharField(max_length=100, verbose_name='Træner for'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='reg_number',
            field=models.CharField(max_length=50, verbose_name='Reg nr'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='account_number',
            field=models.CharField(max_length=50, verbose_name='Konto nr'),
        ),
    ]
