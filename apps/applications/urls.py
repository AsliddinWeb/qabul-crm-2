from django.urls import path
from apps.applications.views import ApplicationMeView, ApplicationByPhoneView

urlpatterns = [
    path('me/', ApplicationMeView.as_view(), name='application-me'),
    path('by-staff/', ApplicationByPhoneView.as_view(), name='application-by-phone'),
]
