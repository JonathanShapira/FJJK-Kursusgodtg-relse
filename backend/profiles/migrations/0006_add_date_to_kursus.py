# Generated manually

from django.db import migrations, models
from datetime import date


def populate_dates(apps, schema_editor):
    """Populate existing kursus records with default dates"""
    Kursus = apps.get_model('profiles', 'Kursus')
    for kursus in Kursus.objects.filter(date__isnull=True):
        if kursus.created_at:
            kursus.date = kursus.created_at.date()
        else:
            kursus.date = date.today()
        kursus.save()


def reverse_populate_dates(apps, schema_editor):
    """Reverse migration - no need to do anything"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_make_profile_fields_mandatory'),
    ]

    operations = [
        # First, add the field as nullable
        migrations.AddField(
            model_name='kursus',
            name='date',
            field=models.DateField(verbose_name='Dato', null=True, blank=True),
        ),
        # Then populate existing records
        migrations.RunPython(populate_dates, reverse_populate_dates),
        # Finally, make the field NOT NULL
        migrations.AlterField(
            model_name='kursus',
            name='date',
            field=models.DateField(verbose_name='Dato'),
        ),
    ]
