from django.db import IntegrityError
from rest_framework import serializers
from followers.models import Follower

class FollowerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Follower model
    The create method handles the unique constraint on 'owner' and 'followed'
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    followed_name = serializers.ReadOnlyField(source='followed.username')

    class Meta:
        model = Follower
        fields = ['id', 'created_at', 'owner', 'followed']

    def create(self, validated_data):
        # to avoid crashing server with 500 error
        try:
            return super().create(validated_data) # super() because we are refering to method from ModelSerializer
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'possible duplicate'
            })