from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer

class UserView(CreateAPIView):
    serializer_class = UserSerializer