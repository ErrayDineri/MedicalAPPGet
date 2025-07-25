from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from main.models import Patient, Report

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample data for testing the medical application'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample users...')
        
        # Create sample admin user
        admin_user, created = User.objects.get_or_create(
            username='admin_user',
            defaults={
                'first_name': 'Admin',
                'last_name': 'User',
                'email': 'admin@medical.com',
                'cin': 'ADM123456',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(f'Created admin user: {admin_user.username}')

        # Create sample technicien user
        technicien_user, created = User.objects.get_or_create(
            username='technicien1',
            defaults={
                'first_name': 'Jean',
                'last_name': 'Dupont',
                'email': 'jean.dupont@medical.com',
                'cin': 'TECH123456',
                'role': 'technicien',
            }
        )
        if created:
            technicien_user.set_password('tech123')
            technicien_user.save()
            self.stdout.write(f'Created technicien user: {technicien_user.username}')

        # Create sample medecin user
        medecin_user, created = User.objects.get_or_create(
            username='medecin1',
            defaults={
                'first_name': 'Dr. Marie',
                'last_name': 'Martin',
                'email': 'marie.martin@medical.com',
                'cin': 'MED123456',
                'role': 'medecin',
            }
        )
        if created:
            medecin_user.set_password('med123')
            medecin_user.save()
            self.stdout.write(f'Created medecin user: {medecin_user.username}')

        # Create sample patients
        self.stdout.write('Creating sample patients...')
        
        sample_patients = [
            {
                'nom': 'Benali',
                'prenom': 'Ahmed',
                'cin': 'PAT001',
                'mail': 'ahmed.benali@email.com',
                'reference_dossier': 'REF001',
            },
            {
                'nom': 'Alami',
                'prenom': 'Fatima',
                'cin': 'PAT002',
                'mail': 'fatima.alami@email.com',
                'reference_dossier': 'REF002',
            },
            {
                'nom': 'Idrissi',
                'prenom': 'Youssef',
                'cin': 'PAT003',
                'mail': 'youssef.idrissi@email.com',
                'reference_dossier': 'REF003',
            }
        ]

        for patient_data in sample_patients:
            patient, created = Patient.objects.get_or_create(
                cin=patient_data['cin'],
                defaults={
                    **patient_data,
                    'added_by': technicien_user
                }
            )
            if created:
                # Create initial report for each patient
                Report.objects.create(
                    patient=patient,
                    text=f"Initial radiological examination for {patient.prenom} {patient.nom}. "
                          f"Patient presented with chest pain. X-ray shows normal cardiac silhouette. "
                          f"No acute findings detected. Recommend follow-up in 6 months.",
                    created_by=technicien_user,
                    status='non_valide'
                )
                self.stdout.write(f'Created patient: {patient.prenom} {patient.nom}')

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
        self.stdout.write('')
        self.stdout.write('Login credentials:')
        self.stdout.write('Admin: admin_user / admin123')
        self.stdout.write('Technicien: technicien1 / tech123')
        self.stdout.write('Médecin: medecin1 / med123')
