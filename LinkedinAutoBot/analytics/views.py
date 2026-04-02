from types import SimpleNamespace

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.authentication import ApiKeyAuthentication
from automation.models import Leads

from .llm import create_agent
from .models import LLM
from .serializers import AnalysisInputSerializer, HostedProfileAnalysisSerializer, LLMSerializer


class AnalysisListView(generics.ListAPIView):
    serializer_class = LLMSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LLM.objects.filter(user=self.request.user).select_related("lead")


class AnalysisDetailView(generics.RetrieveAPIView):
    serializer_class = LLMSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LLM.objects.filter(user=self.request.user).select_related("lead")


class GenerateAnalysisView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_scope = "analytics_generate"

    def post(self, request):
        serializer = AnalysisInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        lead = Leads.objects.filter(id=serializer.validated_data["lead_id"]).first()
        if not lead:
            return Response(
                {"detail": "Lead not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        result = create_agent(
            prompt=serializer.validated_data["prompt"],
            lead=lead,
            api_key=serializer.validated_data.get("api_key"),
        )

        analysis, _ = LLM.objects.update_or_create(
            user=request.user,
            lead=lead,
            defaults={
                "score": result.get("score", 0),
                "insights_strategic": result.get("insights_strategic"),
                "recommended_outreach_ways": result.get("recommended_outreach_ways"),
                "decision_maker_level": result.get("decision_maker_level"),
                "prompt": serializer.validated_data["prompt"],
                "raw_response": result.get("raw_response"),
            },
        )

        return Response(LLMSerializer(analysis).data, status=status.HTTP_200_OK)


class HostedAnalyzeProfileView(APIView):
    authentication_classes = [ApiKeyAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_scope = "hosted_analyze_profile"

    def post(self, request):
        serializer = HostedProfileAnalysisSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        profile_data = serializer.validated_data["profile"]
        profile = SimpleNamespace(
            profile_url=profile_data["profile_url"],
            full_name=profile_data.get("full_name", ""),
            title=profile_data.get("title", ""),
            location=profile_data.get("location", ""),
            about=profile_data.get("about", ""),
            experience=profile_data.get("experience", ""),
            status=profile_data.get("status", "new"),
            metadata=profile_data.get("metadata", {}) or {},
        )
        result = create_agent(
            prompt=serializer.validated_data["prompt"],
            lead=profile,
        )
        return Response(result, status=status.HTTP_200_OK)
