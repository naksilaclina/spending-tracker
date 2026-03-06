from rest_framework import viewsets

from apps.core.permissions import IsOwnerPermission


class UserOwnedModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerPermission]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
