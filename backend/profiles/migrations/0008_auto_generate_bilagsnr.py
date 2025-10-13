# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_add_bilagsnr_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kursus',
            name='bilagsnr',
            field=models.CharField(editable=False, max_length=50, unique=True, verbose_name='Bilagsnr'),
        ),
    ]
