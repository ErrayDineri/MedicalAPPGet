from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    ROLE_CHOICES = [
        ('technicien', 'Technicien Radiologue'),
        ('medecin', 'Médecin Radiologue'),
        ('admin', 'Administrateur'),
    ]
    
    cin = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_archived = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_role_display()})"

class Patient(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    cin = models.CharField(max_length=20, unique=True)
    mail = models.EmailField()
    reference_dossier = models.CharField(max_length=50, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.cin})"
    
    def get_latest_report(self):
        """Get the most recent report for this patient"""
        return self.reports.order_by('-date_created').first()
    
    def get_pending_reports_count(self):
        """Get count of non-validated reports"""
        return self.reports.filter(status='non_valide').count()
    
    def get_validated_reports_count(self):
        """Get count of validated reports"""
        return self.reports.filter(status='valide').count()

class Report(models.Model):
    STATUS_CHOICES = [
        ('non_valide', 'Non Validé'),
        ('valide', 'Validé'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='reports')
    imagerie = models.ImageField(upload_to='report_images/', blank=True, null=True, help_text="Medical scan/image for this report")
    text = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='non_valide')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_reports')
    validated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='validated_reports')
    validation_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-date_created']
    
    def __str__(self):
        return f"Report #{self.id} for {self.patient} - {self.status}"
    
    def get_scan_type(self):
        """Try to determine scan type from filename"""
        if self.imagerie:
            filename = self.imagerie.name.lower()
            if 'xray' in filename or 'x-ray' in filename:
                return 'X-Ray'
            elif 'ct' in filename or 'scan' in filename:
                return 'CT Scan'
            elif 'mri' in filename:
                return 'MRI'
            elif 'ultrasound' in filename or 'echo' in filename:
                return 'Ultrasound'
            else:
                return 'Medical Image'
        return 'No Image'

class ReportSection(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='sections')
    section_title = models.CharField(max_length=200)
    section_text = models.TextField()
    is_accepted = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.report.patient} - {self.section_title}"
