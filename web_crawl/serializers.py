from rest_framework import serializers
from .models import CrawlTask, CrawlResult


class CrawlTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrawlTask
        fields = ['id', 'urls', 'status', 'error_message']


class CrawlResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrawlResult
        fields = ['url', 'title', 'summary', 'links']
