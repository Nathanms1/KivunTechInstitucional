from django.urls import path

from .views import HomeView, PrivacyPolicyView, RobotsTxtView

app_name = 'website'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('politica-de-privacidade/', PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('robots.txt', RobotsTxtView.as_view(), name='robots'),
]
