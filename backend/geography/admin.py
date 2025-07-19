from django.contrib import admin
from .models import Region, Prefecture, Commune, Quartier


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['nom', 'code', 'prefectures_count', 'created_at']
    search_fields = ['nom', 'code']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Prefecture)
class PrefectureAdmin(admin.ModelAdmin):
    list_display = ['nom', 'region', 'communes_count', 'created_at']
    list_filter = ['region', 'created_at']
    search_fields = ['nom', 'region__nom']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Commune)
class CommuneAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prefecture', 'region', 'type', 'quartiers_count', 'created_at']
    list_filter = ['type', 'prefecture__region', 'created_at']
    search_fields = ['nom', 'prefecture__nom', 'prefecture__region__nom']
    readonly_fields = ['created_at', 'updated_at']

    def region(self, obj):
        return obj.prefecture.region.nom
    region.short_description = 'Région'


@admin.register(Quartier)
class QuartierAdmin(admin.ModelAdmin):
    list_display = ['nom', 'commune', 'prefecture', 'region', 'population_estimee', 'superficie_km2']
    list_filter = ['commune__prefecture__region', 'commune__type', 'created_at']
    search_fields = ['nom', 'commune__nom', 'commune__prefecture__nom']
    readonly_fields = ['created_at', 'updated_at']

    def prefecture(self, obj):
        return obj.prefecture.nom
    prefecture.short_description = 'Préfecture'

    def region(self, obj):
        return obj.region.nom
    region.short_description = 'Région' 