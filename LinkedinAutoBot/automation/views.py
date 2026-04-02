import os

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.authentication import ApiKeyAuthentication

from .bot import LinkedinBot
from .models import LeadInteraction, LeadTAG, Leads
from .serializers import (
    HostedProfileByNameSerializer,
    HostedProfileByUrlSerializer,
    HostedSendConnectionSerializer,
    LeadInteractionSerializer,
    LeadSerializer,
    LeadTagSerializer,
    LinkedInMessageRequestSerializer,
    LinkedInProfileRequestSerializer,
)


def _get_hosted_linkedin_credentials():
    email = os.getenv("LINKEDIN_EMAIL")
    password = os.getenv("LINKEDIN_PASSWORD")
    if not email or not password:
        return None
    return {"email": email, "password": password}


class LeadListCreateView(generics.ListCreateAPIView):
    queryset = Leads.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated]


class LeadDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Leads.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated]


class LeadTagListCreateView(generics.ListCreateAPIView):
    queryset = LeadTAG.objects.all()
    serializer_class = LeadTagSerializer
    permission_classes = [IsAuthenticated]


class LeadTagDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LeadTAG.objects.all()
    serializer_class = LeadTagSerializer
    permission_classes = [IsAuthenticated]


class LeadInteractionListCreateView(generics.ListCreateAPIView):
    queryset = LeadInteraction.objects.all()
    serializer_class = LeadInteractionSerializer
    permission_classes = [IsAuthenticated]


class LeadInteractionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LeadInteraction.objects.all()
    serializer_class = LeadInteractionSerializer
    permission_classes = [IsAuthenticated]


class LinkedInProfilePreviewView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_scope = "linkedin_profile_preview"

    def post(self, request):
        serializer = LinkedInProfileRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bot = LinkedinBot(
            email=serializer.validated_data["linkedin_email"],
            password=serializer.validated_data["linkedin_password"],
        )

        try:
            bot.login()
            if serializer.validated_data.get("profile_url"):
                data = bot.collect_data(serializer.validated_data["profile_url"])
                data["profile_url"] = serializer.validated_data["profile_url"]
            else:
                data = bot.collect_data_by_name(serializer.validated_data["name"])
        finally:
            bot.close()

        return Response(data)


class LinkedInSendMessageView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_scope = "linkedin_send_message"

    def post(self, request):
        serializer = LinkedInMessageRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bot = LinkedinBot(
            email=serializer.validated_data["linkedin_email"],
            password=serializer.validated_data["linkedin_password"],
        )

        try:
            bot.login()
            sent = bot.send_connection_request(
                profile_url=serializer.validated_data["profile_url"],
                message=serializer.validated_data["message"],
            )
        finally:
            bot.close()

        return Response({"sent": sent})


class HostedProfileCollectByNameView(APIView):
    authentication_classes = [ApiKeyAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_scope = "hosted_profile_collect"

    def post(self, request):
        serializer = HostedProfileByNameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        credentials = _get_hosted_linkedin_credentials()
        if not credentials:
            return Response(
                {"detail": "Hosted LinkedIn credentials are not configured on the server."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        bot = LinkedinBot(**credentials)
        try:
            bot.login()
            data = bot.collect_data_by_name(serializer.validated_data["name"])
            data.setdefault("full_name", serializer.validated_data["name"])
            data.setdefault("status", "new")
            data.setdefault("metadata", {})
        finally:
            bot.close()

        return Response(data)


class HostedProfileCollectView(APIView):
    authentication_classes = [ApiKeyAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_scope = "hosted_profile_collect"

    def post(self, request):
        serializer = HostedProfileByUrlSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        credentials = _get_hosted_linkedin_credentials()
        if not credentials:
            return Response(
                {"detail": "Hosted LinkedIn credentials are not configured on the server."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        bot = LinkedinBot(**credentials)
        try:
            bot.login()
            data = bot.collect_data(serializer.validated_data["profile_url"])
            data["profile_url"] = serializer.validated_data["profile_url"]
            data.setdefault("full_name", "")
            data.setdefault("status", "new")
            data.setdefault("metadata", {})
        finally:
            bot.close()

        return Response(data)


class HostedSendConnectionRequestView(APIView):
    authentication_classes = [ApiKeyAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_scope = "hosted_send_connection"

    def post(self, request):
        serializer = HostedSendConnectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        credentials = _get_hosted_linkedin_credentials()
        if not credentials:
            return Response(
                {"detail": "Hosted LinkedIn credentials are not configured on the server."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        bot = LinkedinBot(**credentials)
        try:
            bot.login()
            sent = bot.send_connection_request(
                profile_url=serializer.validated_data["profile_url"],
                message=serializer.validated_data.get("message"),
            )
        finally:
            bot.close()

        return Response({"sent": sent})
