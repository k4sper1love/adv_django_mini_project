from rest_framework import serializers
from .models import TradeAnalytics

class TradeAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeAnalytics
        fields = "__all__"
