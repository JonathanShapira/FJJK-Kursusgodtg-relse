# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_add_date_to_kursus'),
    ]

    operations = [
        migrations.AddField(
            model_name='kursus',
            name='bilagsnr',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Bilagsnr'),
        ),
    ]
