from rest_framework import viewsets, permissions
from .models import Application
from .serializers import ApplicationSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Application.objects.none()

        user = self.request.user
        if user.is_authenticated:
            if user.role == 'APPLICANT':
                return Application.objects.filter(user=user)
            elif user.role in ['STAFF', 'ADMIN']:
                return Application.objects.all()
        return Application.objects.none()

    def perform_create(self, serializer):
        # Yaratilayotgan arizaga foydalanuvchini qo‘shish
        serializer.save(user=self.request.user)


