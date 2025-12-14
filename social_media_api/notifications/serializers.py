from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.ReadOnlyField(source='actor.username')
    
    class Meta:
        model = Notification
        fields = ['id', 'actor', 'verb', 'target', 'timestamp', 'read']
        # 'target' is GenericForeignKey, might need custom field if representation is complex
        # For now, default string representation of target might suffice or need adjustment
        
    def to_representation(self, instance):
        # Customize target representation if possible
        ret = super().to_representation(instance)
        ret['target'] = str(instance.target)
        return ret
