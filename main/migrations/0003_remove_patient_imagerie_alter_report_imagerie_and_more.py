# Generated by Django 5.2.4 on 2025-07-25 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_reportimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='imagerie',
        ),
        migrations.AlterField(
            model_name='report',
            name='imagerie',
            field=models.ImageField(blank=True, help_text='Medical scan/image for this report', null=True, upload_to='report_images/'),
        ),
        migrations.DeleteModel(
            name='ReportImage',
        ),
    ]
