from rest_framework import serializers

from .models import LLM


class LLMSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLM
        fields = "__all__"
        read_only_fields = ["id", "user", "created_at", "updated_at"]


class AnalysisInputSerializer(serializers.Serializer):
    lead_id = serializers.IntegerField()
    prompt = serializers.CharField()
    api_key = serializers.CharField(write_only=True, required=False, allow_blank=True)


class ProfilePayloadSerializer(serializers.Serializer):
    profile_url = serializers.URLField()
    full_name = serializers.CharField(required=False, allow_blank=True)
    title = serializers.CharField(required=False, allow_blank=True)
    location = serializers.CharField(required=False, allow_blank=True)
    about = serializers.CharField(required=False, allow_blank=True)
    experience = serializers.CharField(required=False, allow_blank=True)
    status = serializers.CharField(required=False, allow_blank=True, default="new")
    metadata = serializers.DictField(required=False)


class HostedProfileAnalysisSerializer(serializers.Serializer):
    profile = ProfilePayloadSerializer()
    prompt = serializers.CharField()
