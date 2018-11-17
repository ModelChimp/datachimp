from rest_framework import serializers

from datachimp.models.user import User
from datachimp.serializers.profile import ProfileSerializer


class UserSerializer(serializers.ModelSerializer):
    profile_detail = ProfileSerializer(source='profile', read_only=True)
    first_name = serializers.ReadOnlyField(source='user.profile.first_name')
    last_name = serializers.ReadOnlyField(source='user.profile.last_name')

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'profile_detail')
