from rest_framework import serializers

from .models import LeadInteraction, LeadTAG, Leads


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leads
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class LeadInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadInteraction
        fields = "__all__"
        read_only_fields = ["id", "sent_at", "response_at"]


class LeadTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadTAG
        fields = "__all__"
        read_only_fields = ["id"]


class LinkedInProfileRequestSerializer(serializers.Serializer):
    linkedin_email = serializers.EmailField()
    linkedin_password = serializers.CharField(write_only=True)
    profile_url = serializers.URLField(required=False)
    name = serializers.CharField(required=False, allow_blank=False)

    def validate(self, attrs):
        if not attrs.get("profile_url") and not attrs.get("name"):
            raise serializers.ValidationError("Provide either profile_url or name.")
        return attrs


class LinkedInMessageRequestSerializer(LinkedInProfileRequestSerializer):
    message = serializers.CharField(allow_blank=False)


class HostedProfileByNameSerializer(serializers.Serializer):
    name = serializers.CharField(allow_blank=False)


class HostedProfileByUrlSerializer(serializers.Serializer):
    profile_url = serializers.URLField()


class HostedSendConnectionSerializer(serializers.Serializer):
    profile_url = serializers.URLField()
    message = serializers.CharField(required=False, allow_blank=True)
