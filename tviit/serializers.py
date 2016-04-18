from rest_framework import serializers
from .models import Tviit


class TviitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tviit
        fields = ('uuid', 'sender', 'content', 'created', 'modified', 'reply')