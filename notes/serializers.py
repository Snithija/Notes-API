from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Note
        fields = ["id", "title", "content", "user", "username", "created_at", "updated_at"]
        read_only_fields = ["user", "username", "created_at", "updated_at"]

