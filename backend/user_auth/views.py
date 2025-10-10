from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


class RegisterView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    POST /auth/register/
    """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            "message": "User registered successfully!",
            "username": serializer.data.get('username')
        }, status=status.HTTP_201_CREATED, headers=headers)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    API endpoint for user logout.
    Future: Add token blacklisting here.
    """
    return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)