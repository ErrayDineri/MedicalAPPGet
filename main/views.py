from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.conf import settings
from .models import User, Patient, Report, ReportSection
from .forms import PatientForm, UserForm, ReportForm
import json
import secrets
import string

def login_view(request):
    # Check if user just set their password
    if request.GET.get('password_set') == 'true':
        messages.success(request, 'Votre mot de passe a été créé avec succès! Vous pouvez maintenant vous connecter.')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and not user.is_archived:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials or account is archived.')
    
    return render(request, 'main/login.html')

@login_required
def dashboard(request):
    """Redirect to appropriate dashboard based on user role"""
    if request.user.role == 'technicien':
        return redirect('technicien_dashboard')
    elif request.user.role == 'medecin':
        return redirect('medecin_dashboard')
    elif request.user.role == 'admin':
        return redirect('admin_dashboard')
    else:
        messages.error(request, 'No dashboard available for your role.')
        return redirect('login')

@login_required
def technicien_dashboard(request):
    """Dashboard for Technicien Radiologue"""
    if request.user.role != 'technicien':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    search_performed = False
    found_patient = None
    reference_dossier = None
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'search':
            # Search for patient by reference dossier
            reference_dossier = request.POST.get('reference_dossier', '').strip()
            if reference_dossier:
                try:
                    found_patient = Patient.objects.get(reference_dossier=reference_dossier)
                    search_performed = True
                except Patient.DoesNotExist:
                    search_performed = True
                    found_patient = None
        
        elif action == 'add_scan':
            # Add scan to existing patient
            patient_id = request.POST.get('patient_id')
            medical_image = request.FILES.get('imagerie')
            
            if patient_id and medical_image:
                try:
                    patient = Patient.objects.get(id=patient_id)
                    new_report = Report.objects.create(
                        patient=patient,
                        imagerie=medical_image,
                        text=f"Medical scan for {patient.prenom} {patient.nom}.\n"
                              f"Scan Date: {timezone.now().strftime('%d/%m/%Y %H:%M')}\n"
                              f"Technician: {request.user.get_full_name()}\n\n"
                              f"[Awaiting radiologist review and analysis]",
                        created_by=request.user
                    )
                    messages.success(request, f'New scan added for {patient.prenom} {patient.nom}.')
                    return redirect('technicien_dashboard')
                except Patient.DoesNotExist:
                    messages.error(request, 'Patient not found.')
        
        elif action == 'create_patient':
            # Create new patient with first scan
            form = PatientForm(request.POST, request.FILES)
            if form.is_valid():
                medical_image = form.cleaned_data['imagerie']
                if medical_image:
                    # Create patient
                    patient_data = form.cleaned_data.copy()
                    patient_data.pop('imagerie')
                    
                    patient = Patient(**patient_data)
                    patient.added_by = request.user
                    patient.save()
                    
                    # Create first scan/report
                    new_report = Report.objects.create(
                        patient=patient,
                        imagerie=medical_image,
                        text=f"Initial medical scan for {patient.prenom} {patient.nom}.\n"
                              f"Scan Date: {timezone.now().strftime('%d/%m/%Y %H:%M')}\n"
                              f"Technician: {request.user.get_full_name()}\n\n"
                              f"[Awaiting radiologist review and analysis]",
                        created_by=request.user
                    )
                    
                    messages.success(request, f'Patient {patient.prenom} {patient.nom} created with first scan.')
                    return redirect('technicien_dashboard')
                else:
                    messages.error(request, 'Medical image is required.')
    
    # Get recent reports created by this technician
    recent_reports = Report.objects.filter(created_by=request.user).order_by('-date_created')[:10]
    
    context = {
        'recent_reports': recent_reports,
        'search_performed': search_performed,
        'found_patient': found_patient,
        'reference_dossier': reference_dossier,
        'form': PatientForm() if not found_patient and search_performed else None,
    }
    
    return render(request, 'main/technicien_dashboard.html', context)

@login_required
def medecin_dashboard(request):
    """Dashboard for Médecin Radiologue"""
    if request.user.role != 'medecin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    # Get filter parameter
    show_validated = request.GET.get('show_validated', 'false') == 'true'
    
    # Filter reports based on validation status
    if show_validated:
        reports = Report.objects.filter(status='valide')
    else:
        reports = Report.objects.filter(status='non_valide')
    
    context = {
        'reports': reports,
        'show_validated': show_validated,
    }
    return render(request, 'main/medecin_dashboard.html', context)

@login_required
def report_detail(request, report_id):
    """Detailed view of a patient report for editing"""
    if request.user.role != 'medecin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    report = get_object_or_404(Report, id=report_id)
    
    if request.method == 'POST':
        # Handle report validation
        if 'validate_report' in request.POST:
            report.status = 'valide'
            report.validated_by = request.user
            report.validation_date = timezone.now()
            report.save()
            messages.success(request, 'Report validated successfully!')
            return redirect('medecin_dashboard')
        
        # Handle text updates
        elif 'update_text' in request.POST:
            report.text = request.POST.get('report_text', report.text)
            report.save()
            messages.success(request, 'Report updated successfully!')
    
    context = {
        'report': report,
        'patient': report.patient,
    }
    return render(request, 'main/report_detail.html', context)

@login_required
def report_history(request, patient_id):
    """View patient's report history"""
    if request.user.role != 'medecin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    patient = get_object_or_404(Patient, id=patient_id)
    reports = Report.objects.filter(patient=patient).order_by('-date_created')
    
    context = {
        'patient': patient,
        'reports': reports,
    }
    return render(request, 'main/report_history.html', context)

@login_required
def admin_dashboard(request):
    """Dashboard for Administrator"""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    # Get filter parameter for archived users
    show_archived = request.GET.get('show_archived', 'false') == 'true'
    
    # Get users based on archived status
    if show_archived:
        users = User.objects.filter(
            role__in=['technicien', 'medecin'],
            is_archived=True
        ).order_by('role', 'last_name', 'first_name')
    else:
        users = User.objects.filter(
            role__in=['technicien', 'medecin'],
            is_archived=False
        ).order_by('role', 'last_name', 'first_name')
    
    # Calculate statistics (always for active users)
    total_doctors = User.objects.filter(role='medecin', is_archived=False).count()
    total_technicians = User.objects.filter(role='technicien', is_archived=False).count()
    active_users = User.objects.filter(role__in=['technicien', 'medecin'], is_archived=False).count()
    archived_users = User.objects.filter(role__in=['technicien', 'medecin'], is_archived=True).count()
    
    context = {
        'users': users,
        'total_doctors': total_doctors,
        'total_technicians': total_technicians,
        'active_users': active_users,
        'archived_users': archived_users,
        'show_archived': show_archived,
    }
    return render(request, 'main/admin_dashboard.html', context)

@login_required
def add_employee(request):
    """Add new employee"""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Set unusable password - user will set it via email link
            user.set_unusable_password()
            user.save()
            
            # Generate password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Create password reset link
            reset_link = request.build_absolute_uri(f'/password-reset-confirm/{uid}/{token}/')
            
            # Send email
            subject = 'Bienvenue - Créez votre mot de passe'
            context = {
                'user': user,
                'reset_link': reset_link,
                'timeout_seconds': settings.PASSWORD_RESET_TIMEOUT,
            }
            message = render_to_string('emails/welcome_email.txt', context)
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                messages.success(request, f'Employee {user.get_full_name()} added successfully! A password setup email has been sent to {user.email}.')
            except Exception as e:
                # If email fails, delete the user and show error
                user.delete()
                messages.error(request, f'Failed to send email to {form.cleaned_data["email"]}. Employee not created. Please check the email address and try again.')
                
            return redirect('admin_dashboard')
    else:
        form = UserForm()
    
    context = {
        'form': form,
    }
    return render(request, 'main/add_employee.html', context)

@login_required
@require_POST
def archive_user(request, user_id):
    """Archive a user"""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    user = get_object_or_404(User, id=user_id)
    user.is_archived = True
    user.save()
    messages.success(request, f'User {user.get_full_name()} archived successfully!')
    return redirect('admin_dashboard')

@login_required
@require_POST
def reactivate_user(request, user_id):
    """Reactivate an archived user"""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    user = get_object_or_404(User, id=user_id)
    user.is_archived = False
    user.save()
    messages.success(request, f'User {user.get_full_name()} reactivated successfully!')
    return redirect('admin_dashboard')

@login_required
@require_POST
def reset_password(request, user_id):
    """Reset user password"""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    user = get_object_or_404(User, id=user_id)
    
    # Set unusable password - user will set it via email link
    user.set_unusable_password()
    user.save()
    
    # Generate password reset token
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    # Create password reset link
    reset_link = request.build_absolute_uri(f'/password-reset-confirm/{uid}/{token}/')
    
    # Send email
    subject = 'Réinitialisation de mot de passe - Medical App'
    context = {
        'user': user,
        'reset_link': reset_link,
        'is_reset': True,  # Flag to indicate this is a password reset
        'timeout_seconds': settings.PASSWORD_RESET_TIMEOUT,
    }
    message = render_to_string('emails/password_reset_email.txt', context)
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        messages.success(request, f'Password reset email sent to {user.get_full_name()} ({user.email}). They will receive instructions to create a new password.')
    except Exception as e:
        messages.error(request, f'Failed to send password reset email to {user.email}. Please check the email address and try again.')
    
    return redirect('admin_dashboard')
