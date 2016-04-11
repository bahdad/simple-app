from rest_framework import serializers

from simple_app.restapi.model import Domain


class DomainSerializer(serializers.ModelSerializer):

    class Meta:
        model = Domain

    def create(self, validated_data):
        instance = super().create(validated_data)
        return instance
