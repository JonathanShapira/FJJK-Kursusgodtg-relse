from django.core.management.base import BaseCommand
from django.db.models import Q
from profiles.models import Kursus
import uuid
from datetime import datetime


class Command(BaseCommand):
    help = 'Generate bilagsnr for Kursus records that have null values'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        self.stdout.write("🔧 Generating missing bilagsnr for existing Kursus records...")
        
        try:
            # Find all Kursus records with null or empty bilagsnr
            kursus_without_bilagsnr = Kursus.objects.filter(
                Q(bilagsnr__isnull=True) | Q(bilagsnr='')
            )
            
            count = kursus_without_bilagsnr.count()
            self.stdout.write(f"Found {count} Kursus records without bilagsnr")
            
            if count == 0:
                self.stdout.write(self.style.SUCCESS("✅ All Kursus records already have bilagsnr!"))
                return
            
            if dry_run:
                self.stdout.write("🔍 DRY RUN - No changes will be made")
                for kursus in kursus_without_bilagsnr:
                    new_bilagsnr = self.generate_bilagsnr()
                    self.stdout.write(f"Would update Kursus {kursus.id}: {new_bilagsnr}")
                return
            
            # Generate bilagsnr for each record
            updated_count = 0
            for kursus in kursus_without_bilagsnr:
                # Generate unique bilagsnr
                new_bilagsnr = self.generate_bilagsnr()
                
                # Ensure uniqueness
                while Kursus.objects.filter(bilagsnr=new_bilagsnr).exists():
                    new_bilagsnr = self.generate_bilagsnr()
                
                # Update the record
                kursus.bilagsnr = new_bilagsnr
                kursus.save()
                
                updated_count += 1
                self.stdout.write(f"✅ Updated Kursus {kursus.id}: {new_bilagsnr}")
            
            self.stdout.write(
                self.style.SUCCESS(f"\n🎉 Successfully generated bilagsnr for {updated_count} Kursus records!")
            )
            
            # Verify all records now have bilagsnr
            remaining_null = Kursus.objects.filter(
                Q(bilagsnr__isnull=True) | Q(bilagsnr='')
            ).count()
            
            if remaining_null == 0:
                self.stdout.write(self.style.SUCCESS("✅ All Kursus records now have bilagsnr!"))
            else:
                self.stdout.write(
                    self.style.WARNING(f"⚠️  Warning: {remaining_null} records still have null bilagsnr")
                )
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error: {e}"))
            raise

    def generate_bilagsnr(self):
        """Generate a unique bilagsnr"""
        # Format: YYYYMMDD-XXXX (date + 4 random digits)
        date_str = datetime.now().strftime('%Y%m%d')
        random_suffix = str(uuid.uuid4().hex[:4]).upper()
        return f"{date_str}-{random_suffix}"
