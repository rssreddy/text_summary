# app/views.py (using Django REST Framework)
from rest_framework import viewsets, status, pagination
from rest_framework.response import Response
from .models import CrawlTask, CrawlResult
from .serializers import CrawlTaskSerializer, CrawlResultSerializer
from .tasks import crawl_page_task

class CrawlViewSet(viewsets.ViewSet):
    def create(self, request):
        urls = request.data.get('urls', [])

        # Create a CrawlTask for each URL and send it to Celery
        task_responses = []
        for url in urls:
            task_serializer = CrawlTaskSerializer(data={'urls': [url]})  # Create serializer for single URL
            if task_serializer.is_valid():
                task = task_serializer.save()
                crawl_page_task.apply_async(args=[task.id, url])  # Send task for the single URL
                task_responses.append(task_serializer.data)  # Add the task data to the response list
            else:
                # Handle invalid URL (optional)
                return Response(task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(task_responses, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            task = CrawlTask.objects.get(pk=pk)
        except CrawlTask.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CrawlTaskSerializer(task)
        return Response(serializer.data)


class ResultViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CrawlResultSerializer

    def get_queryset(self):
        task_id = self.request.query_params.get('task_id')
        if task_id:
            print(CrawlTask.objects.get(id=task_id).crawlresult_set.all())
            return CrawlTask.objects.get(id=task_id).crawlresult_set.all()
        return CrawlTask.objects.none()  # Return empty queryset if no task_id


class CustomPagination(pagination.PageNumberPagination):
    page_size = 2 # Set the desired page size here
class CrawlReportViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CrawlResultSerializer
    pagination_class = CustomPagination  # Enable pagination

    def get_queryset(self):
        # Get all unique URLs
        unique_urls = CrawlResult.objects.values_list('url', flat=True).distinct()

        # Create a dictionary to store results by URL
        results_by_url = {}
        for result in CrawlResult.objects.filter(url__in=unique_urls):
            results_by_url[result.url] = result

        # Sort the results to ensure pagination works consistently
        sorted_results = [results_by_url[url] for url in unique_urls]
        return sorted_results
