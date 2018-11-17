from rest_framework import serializers
from datachimp.models.machinelearning_model import MachineLearningModel


class ExperimentParamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineLearningModel
        fields = ('model_parameters', )
