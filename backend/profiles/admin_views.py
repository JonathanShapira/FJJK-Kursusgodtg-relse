from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.conf import settings
from django.db.models import Sum
from .models import UserProfile, Kursus
from .serializers import KursusAdminSerializer
import zipfile
import os
from datetime import datetime

# Import openpyxl only when needed
try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment
    OPENPYXL_AVAILABLE = True
except ImportError:
    OPENPYXL_AVAILABLE = False


def is_admin(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_admin)
def admin_export_page(request):
    """Admin page for exporting data"""
    # Get statistics
    total_users = UserProfile.objects.count()
    total_kursus = Kursus.objects.count()
    total_files = Kursus.objects.filter(file__isnull=False).exclude(file='').count()
    
    context = {
        'total_users': total_users,
        'total_kursus': total_kursus,
        'total_files': total_files,
    }
    
    return render(request, 'profiles/admin_export.html', context)


@user_passes_test(is_admin)
def export_excel(request):
    """Export all kursus data to Excel file"""
    if not OPENPYXL_AVAILABLE:
        messages.error(request, 'openpyxl er ikke installeret. Installer det med: pip install openpyxl')
        return redirect('admin-export')
    
    try:
        # Get all kursus records with user and profile data
        kursus_records = Kursus.objects.select_related('user', 'user__profile').all()
        
        # Serialize the data using admin serializer
        serializer = KursusAdminSerializer(kursus_records, many=True)
        data = serializer.data
        
        # Create workbook and worksheet
        wb = Workbook()
        ws = wb.active
        ws.title = "Kursus Data"
        
        # Define headers
        headers = [
            'Fulde Navn',
            'Træner for', 
            'Kursusnavn og Arrangør',
            'Kursussted',
            'Dato for Kursus',
            'Pris',
            'Bilagsnr'
        ]
        
        # Add headers to worksheet
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center')
        
        # Add data rows
        for row, kursus_data in enumerate(data, 2):
            # Combine kursus and arrangor
            kursus_and_arrangor = f"{kursus_data['kursus']} - {kursus_data['arrangor']}"
            
            # Format date
            kursus_date = datetime.strptime(kursus_data['date'], '%Y-%m-%d').strftime('%d/%m/%Y')
            
            # Add row data
            ws.cell(row=row, column=1, value=kursus_data['user_full_name'])
            ws.cell(row=row, column=2, value=kursus_data['user_trainer_for'])
            ws.cell(row=row, column=3, value=kursus_and_arrangor)
            ws.cell(row=row, column=4, value=kursus_data['sted'])
            ws.cell(row=row, column=5, value=kursus_date)
            ws.cell(row=row, column=6, value=float(kursus_data['pris']))
            ws.cell(row=row, column=7, value=kursus_data['bilagsnr'])
        
        # Auto-adjust column widths
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width
        
        # Create response
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="kursus_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx"'
        
        # Save workbook to response
        wb.save(response)
        return response
        
    except Exception as e:
        messages.error(request, f'Fejl ved eksport af Excel fil: {str(e)}')
        return redirect('admin-export')


@user_passes_test(is_admin)
def export_zip(request):
    """Export all kursus attachments as ZIP file"""
    try:
        # Get all kursus records with files
        kursus_records = Kursus.objects.filter(file__isnull=False).exclude(file='')
        
        if not kursus_records.exists():
            messages.warning(request, 'Ingen filer fundet til eksport.')
            return redirect('admin-export')
        
        # Create ZIP file in memory
        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="kursus_filer_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip"'
        
        with zipfile.ZipFile(response, 'w') as zip_file:
            for kursus in kursus_records:
                if kursus.file and kursus.file.name:
                    # Get the file path
                    file_path = os.path.join(settings.MEDIA_ROOT, kursus.file.name)
                    
                    if os.path.exists(file_path):
                        # Get file extension
                        file_extension = os.path.splitext(kursus.file.name)[1]
                        
                        # Create filename using only bilagsnr
                        if kursus.bilagsnr:
                            filename = f"{kursus.bilagsnr}{file_extension}"
                        else:
                            filename = f"{kursus.id}{file_extension}"
                        
                        # Add file to ZIP
                        zip_file.write(file_path, filename)
        
        return response
        
    except Exception as e:
        messages.error(request, f'Fejl ved eksport af ZIP fil: {str(e)}')
        return redirect('admin-export')


@user_passes_test(is_admin)
def export_user_summary_excel(request):
    """Export user summary with total course prices to Excel file"""
    if not OPENPYXL_AVAILABLE:
        messages.error(request, 'openpyxl er ikke installeret. Installer det med: pip install openpyxl')
        return redirect('admin-export')
    
    try:
        # Get all user profiles with their course totals
        user_profiles = UserProfile.objects.select_related('user').annotate(
            total_pris=Sum('user__kursus_records__pris')
        ).filter(total_pris__isnull=False).order_by('user__last_name', 'user__first_name')
        
        if not user_profiles.exists():
            messages.warning(request, 'Ingen brugere med kurser fundet.')
            return redirect('admin-export')
        
        # Create workbook and worksheet
        wb = Workbook()
        ws = wb.active
        ws.title = "Bruger Oversigt"
        
        # Define headers
        headers = [
            'Fulde Navn',
            'Reg nr',
            'Konto nr',
            'Total Pris for Kurser'
        ]
        
        # Add headers to worksheet
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center')
        
        # Add data rows
        for row, profile in enumerate(user_profiles, 2):
            # Get full name
            full_name = f"{profile.user.first_name} {profile.user.last_name}".strip()
            if not full_name:
                full_name = profile.user.username
            
            # Add row data
            ws.cell(row=row, column=1, value=full_name)
            ws.cell(row=row, column=2, value=profile.reg_number)
            ws.cell(row=row, column=3, value=profile.account_number)
            ws.cell(row=row, column=4, value=float(profile.total_pris))
        
        # Auto-adjust column widths
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width
        
        # Create response
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="bruger_oversigt_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx"'
        
        # Save workbook to response
        wb.save(response)
        return response
        
    except Exception as e:
        messages.error(request, f'Fejl ved eksport af bruger oversigt: {str(e)}')
        return redirect('admin-export')
