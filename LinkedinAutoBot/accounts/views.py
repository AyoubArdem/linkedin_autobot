from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Membership, User, WorkSpace
from .serializers import MembershipSerializer, UserSerializer, WorkSpaceSerializer


class UserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UpdateDeleteRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class WorkspaceView(generics.ListCreateAPIView):
    queryset = WorkSpace.objects.all()
    serializer_class = WorkSpaceSerializer
    permission_classes = [IsAuthenticated]


class WorkView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkSpace.objects.all()
    serializer_class = WorkSpaceSerializer
    permission_classes = [IsAuthenticated]


class MemberView(generics.ListCreateAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    permission_classes = [IsAuthenticated]


class MembershipView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    permission_classes = [IsAuthenticated]
