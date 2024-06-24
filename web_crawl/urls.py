# app/urls.py (or project_root/urls.py if you've included app's urls there)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CrawlViewSet, ResultViewSet, CrawlReportViewSet

router = DefaultRouter()
router.register(r'crawl', CrawlViewSet, basename='crawl')
router.register(r'results', ResultViewSet, basename='results')
router.register(r'reports', CrawlReportViewSet, basename='reports')

urlpatterns = [
    path('', include(router.urls)),
    path('crawl/<int:pk>/', CrawlViewSet.as_view({'get': 'retrieve'}), name='crawl-detail'), # Add this line
]
