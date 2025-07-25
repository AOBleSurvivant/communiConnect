# Generated by Django 4.2.7 on 2025-07-25 10:22

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notifications', '0002_alertreport_communityalert_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HelpRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('request_type', models.CharField(choices=[('request', "Demande d'aide"), ('offer', "Offre d'aide")], default='request', max_length=10)),
                ('need_type', models.CharField(choices=[('material', 'Matériel'), ('presence', 'Présence/Accompagnement'), ('service', 'Service'), ('transport', 'Transport'), ('shopping', 'Courses'), ('technical', 'Aide technique'), ('education', 'Aide éducative'), ('other', 'Autre')], max_length=20)),
                ('for_who', models.CharField(choices=[('myself', 'Moi-même'), ('family', 'Ma famille'), ('neighbor', 'Mon voisin'), ('community', 'La communauté'), ('other', 'Autre')], default='myself', max_length=20)),
                ('title', models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(5), django.core.validators.MaxLengthValidator(200)])),
                ('description', models.TextField(validators=[django.core.validators.MinLengthValidator(10), django.core.validators.MaxLengthValidator(2000)])),
                ('duration_type', models.CharField(choices=[('immediate', 'Immédiat'), ('this_week', 'Cette semaine'), ('this_month', 'Ce mois'), ('specific_date', 'Avant une date spécifique'), ('ongoing', 'En continu')], default='this_week', max_length=20)),
                ('specific_date', models.DateField(blank=True, null=True)),
                ('estimated_hours', models.PositiveIntegerField(blank=True, help_text='Durée estimée en heures', null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('address', models.CharField(blank=True, max_length=500)),
                ('neighborhood', models.CharField(blank=True, max_length=100)),
                ('city', models.CharField(blank=True, max_length=100)),
                ('postal_code', models.CharField(blank=True, max_length=10)),
                ('proximity_zone', models.CharField(choices=[('local', 'Quartier'), ('city', 'Ville'), ('region', 'Région')], default='local', max_length=50)),
                ('status', models.CharField(choices=[('open', 'Ouverte'), ('in_progress', 'En cours'), ('completed', 'Clôturée'), ('cancelled', 'Annulée')], default='open', max_length=20)),
                ('is_urgent', models.BooleanField(default=False)),
                ('expires_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('views_count', models.PositiveIntegerField(default=0)),
                ('responses_count', models.PositiveIntegerField(default=0)),
                ('custom_need_type', models.CharField(blank=True, max_length=100)),
                ('custom_for_who', models.CharField(blank=True, max_length=100)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='help_requests/')),
                ('contact_preference', models.CharField(choices=[('message', 'Message privé'), ('phone', 'Téléphone'), ('email', 'Email'), ('any', "N'importe lequel")], default='message', max_length=20)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='help_requests', to=settings.AUTH_USER_MODEL)),
                ('related_alert', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_help_requests', to='notifications.communityalert')),
            ],
            options={
                'db_table': 'help_requests',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='HelpRequestCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('icon', models.CharField(max_length=10)),
                ('color', models.CharField(default='blue', max_length=20)),
                ('description', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'db_table': 'help_request_categories',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='HelpResponse',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('response_type', models.CharField(choices=[('offer_help', 'Je peux aider'), ('need_help', "J'ai besoin d'aide"), ('contact', 'Contacter'), ('question', 'Question')], max_length=20)),
                ('message', models.TextField(validators=[django.core.validators.MinLengthValidator(5), django.core.validators.MaxLengthValidator(1000)])),
                ('contact_phone', models.CharField(blank=True, max_length=20)),
                ('contact_email', models.EmailField(blank=True, max_length=254)),
                ('is_accepted', models.BooleanField(default=False)),
                ('is_rejected', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='help_responses', to=settings.AUTH_USER_MODEL)),
                ('help_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='help_requests.helprequest')),
            ],
            options={
                'db_table': 'help_responses',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='helprequest',
            index=models.Index(fields=['request_type', 'need_type'], name='help_reques_request_c8e306_idx'),
        ),
        migrations.AddIndex(
            model_name='helprequest',
            index=models.Index(fields=['status', 'is_urgent'], name='help_reques_status_4fc8a5_idx'),
        ),
        migrations.AddIndex(
            model_name='helprequest',
            index=models.Index(fields=['latitude', 'longitude'], name='help_reques_latitud_c0aa2e_idx'),
        ),
        migrations.AddIndex(
            model_name='helprequest',
            index=models.Index(fields=['city', 'neighborhood'], name='help_reques_city_b2407f_idx'),
        ),
        migrations.AddIndex(
            model_name='helprequest',
            index=models.Index(fields=['created_at'], name='help_reques_created_a1fd4c_idx'),
        ),
        migrations.AddIndex(
            model_name='helprequest',
            index=models.Index(fields=['duration_type'], name='help_reques_duratio_c9713b_idx'),
        ),
        migrations.AddIndex(
            model_name='helprequest',
            index=models.Index(fields=['proximity_zone'], name='help_reques_proximi_2798ac_idx'),
        ),
    ]
