from rest_framework import serializers
from datachimp.models.data import Data


class DataSerializer(serializers.ModelSerializer):
    date_created_epoch = serializers.SerializerMethodField('to_epoch_date')

    class Meta:
        model = Data
        fields = '__all__'

    def to_epoch_date(self,obj):
        return int(obj.date_created.strftime("%s"))
