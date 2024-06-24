from django.db import models

class CrawlTask(models.Model):
    urls = models.JSONField()
    status = models.CharField(max_length=20, default="pending")
    start_time = models.DateTimeField(auto_now_add=True)
    error_message = models.TextField(blank=True, null=True)

class CrawlResult(models.Model):
    task = models.ForeignKey(CrawlTask, on_delete=models.CASCADE)
    url = models.URLField()
    title = models.CharField(max_length=255)
    summary = models.TextField()
    links = models.JSONField()
