from rest_framework import serializers
from ..models import DayOff


class DayOffSerializer(serializers.ModelSerializer):
    employee = serializers.StringRelatedField(read_only=True)

    # status = serializers.ChoiceField(choices=DayOff.STATUS_CHOICES)
    class Meta:
        model = DayOff
        fields = ('employee', 'start_date', 'end_date', 'reason', 'status')
        extra_kwargs = {
            'status': {'read_only': True}
        }

    def create(self, validated_data):
        validated_data['employee'] = self.context['request'].user
        return super().create(validated_data)


class DayOffStatusSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=DayOff.STATUS_CHOICES)

    class Meta:
        model = DayOff
        fields = ('status',)

    def update(self, instance, validated_data):
        # check if user is admin
        request = self.context['request']
        if request.user.is_staff:
            instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
