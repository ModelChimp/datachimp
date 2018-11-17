from rest_framework import serializers
from datachimp.models.comment import Comment
from datachimp.serializers.user import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
