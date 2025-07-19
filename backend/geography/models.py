from django.db import models
from django.core.validators import MinLengthValidator


class Region(models.Model):
    """Modèle pour les régions de Guinée"""
    nom = models.CharField(max_length=100, unique=True, validators=[MinLengthValidator(2)])
    code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Région"
        verbose_name_plural = "Régions"
        ordering = ['nom']

    def __str__(self):
        return self.nom

    @property
    def prefectures_count(self):
        return self.prefectures.count()


class Prefecture(models.Model):
    """Modèle pour les préfectures de Guinée"""
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='prefectures')
    nom = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
    code = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Préfecture"
        verbose_name_plural = "Préfectures"
        ordering = ['region', 'nom']
        unique_together = ['region', 'nom']

    def __str__(self):
        return f"{self.nom} ({self.region.nom})"

    @property
    def communes_count(self):
        return self.communes.count()


class Commune(models.Model):
    """Modèle pour les communes de Guinée"""
    TYPE_CHOICES = [
        ('urbaine', 'Commune Urbaine'),
        ('rurale', 'Commune Rurale'),
    ]
    
    prefecture = models.ForeignKey(Prefecture, on_delete=models.CASCADE, related_name='communes')
    nom = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='rurale')
    code = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Commune"
        verbose_name_plural = "Communes"
        ordering = ['prefecture', 'nom']
        unique_together = ['prefecture', 'nom']

    def __str__(self):
        return f"{self.nom} ({self.prefecture.nom})"

    @property
    def quartiers_count(self):
        return self.quartiers.count()


class Quartier(models.Model):
    """Modèle pour les quartiers de Guinée"""
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, related_name='quartiers')
    nom = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
    code = models.CharField(max_length=10, blank=True, null=True)
    population_estimee = models.PositiveIntegerField(blank=True, null=True)
    superficie_km2 = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Quartier"
        verbose_name_plural = "Quartiers"
        ordering = ['commune', 'nom']
        unique_together = ['commune', 'nom']

    def __str__(self):
        return f"{self.nom} ({self.commune.nom})"

    @property
    def region(self):
        return self.commune.prefecture.region

    @property
    def prefecture(self):
        return self.commune.prefecture

    @property
    def full_address(self):
        """Retourne l'adresse complète du quartier"""
        return f"{self.nom}, {self.commune.nom}, {self.prefecture.nom}, {self.region.nom}" 