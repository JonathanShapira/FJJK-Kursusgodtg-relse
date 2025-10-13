# Generated manually

from django.db import migrations, models
from django.db.models import Q
import uuid
from datetime import datetime


def generate_bilagsnr():
    """Generate a unique bilagsnr"""
    # Format: YYYYMMDD-XXXX (date + 4 random digits)
    date_str = datetime.now().strftime('%Y%m%d')
    random_suffix = str(uuid.uuid4().hex[:4]).upper()
    return f"{date_str}-{random_suffix}"


def populate_bilagsnr(apps, schema_editor):
    """Populate bilagsnr for existing records"""
    Kursus = apps.get_model('profiles', 'Kursus')
    
    # Get all records without bilagsnr
    records_without_bilagsnr = Kursus.objects.filter(
        Q(bilagsnr__isnull=True) | Q(bilagsnr='')
    )
    
    for kursus in records_without_bilagsnr:
        # Generate unique bilagsnr
        new_bilagsnr = generate_bilagsnr()
        
        # Ensure uniqueness
        while Kursus.objects.filter(bilagsnr=new_bilagsnr).exists():
            new_bilagsnr = generate_bilagsnr()
        
        kursus.bilagsnr = new_bilagsnr
        kursus.save()


def reverse_populate_bilagsnr(apps, schema_editor):
    """Reverse operation - set bilagsnr to null"""
    Kursus = apps.get_model('profiles', 'Kursus')
    Kursus.objects.all().update(bilagsnr=None)


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_merge_20251013_2042'),
    ]

    operations = [
        # First, make sure bilagsnr field exists and is nullable
        migrations.AlterField(
            model_name='kursus',
            name='bilagsnr',
            field=models.CharField(max_length=50, verbose_name='Bilagsnr', null=True, blank=True),
        ),
        
        # Populate existing records with bilagsnr
        migrations.RunPython(
            populate_bilagsnr,
            reverse_populate_bilagsnr,
        ),
        
        # Now make the field non-nullable and unique
        migrations.AlterField(
            model_name='kursus',
            name='bilagsnr',
            field=models.CharField(max_length=50, verbose_name='Bilagsnr', unique=True, editable=False),
        ),
    ]
