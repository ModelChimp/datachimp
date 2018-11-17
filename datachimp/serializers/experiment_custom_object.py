from rest_framework import serializers
from datachimp.models.experiment_custom_object import ExperimentCustomObject


class ExperimentCustomObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperimentCustomObject
        fields = '__all__'
