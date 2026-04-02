from rest_framework import serializers

from .models import Membership, User, WorkSpace


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "email",
            "password",
            "api_key",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "api_key", "created_at", "updated_at"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


class WorkSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSpace
        fields = ["id", "name", "owner", "created_at"]
        read_only_fields = ["id", "created_at"]


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ["id", "user", "workspace", "joined_at"]
        read_only_fields = ["id", "joined_at"]
