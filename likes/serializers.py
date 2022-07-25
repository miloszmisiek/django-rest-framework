from django.db import IntegrityError
from rest_framework import serializers
from likes.models import Likes


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Like model
    The create method handles the unique constraint on 'owner' and 'post'
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Likes
        fields = ['id', 'created_at', 'owner', 'post']

    def create(self, validated_data):
        # to avoid crashing server with 500 error
        try:
            return super().create(validated_data) # super() because we are refering to method from ModelSerializer
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'possible duplicate'
            })