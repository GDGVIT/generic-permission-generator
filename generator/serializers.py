from rest_framework import serializers

from generator.models import UploadTemplate


class UploadTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = UploadTemplate
        exclude = ["file"]

