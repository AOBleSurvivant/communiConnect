from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'regions', views.RegionViewSet)
router.register(r'prefectures', views.PrefectureViewSet)
router.register(r'communes', views.CommuneViewSet)
router.register(r'quartiers', views.QuartierViewSet)

urlpatterns = [
    # URLs pour les ViewSets
    path('', include(router.urls)),
    
    # URLs pour les formulaires en cascade
    path('regions/<int:region_id>/prefectures/', views.get_prefectures_by_region, name='prefectures-by-region'),
    path('prefectures/<int:prefecture_id>/communes/', views.get_communes_by_prefecture, name='communes-by-prefecture'),
    path('communes/<int:commune_id>/quartiers/', views.get_quartiers_by_commune, name='quartiers-by-commune'),
] 