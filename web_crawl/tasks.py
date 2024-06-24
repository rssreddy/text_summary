# app/tasks.py
from celery import shared_task
from .models import CrawlTask, CrawlResult
from .singlepage import crawl_single_page  # Your existing crawling function
import logging

logger = logging.getLogger(__name__)

@shared_task
def crawl_page_task(task_id, url):
    task = CrawlTask.objects.get(id=task_id)
    task.status = "in progress"
    task.save()

    try:
        logger.info(f"Crawling URL: {url}")
        title, summary, links = crawl_single_page(url)
        existing_result = CrawlResult.objects.filter(url=url).first()

        if existing_result:
            # Update the existing result
            existing_result.title = title
            existing_result.summary = summary
            existing_result.links = links
            existing_result.save()
        else:
            # Create a new result
            CrawlResult.objects.create(
                task=CrawlTask.objects.get(id=task_id),
                url=url,
                title=title,
                summary=summary,
                links=links
            )
        task.status = "complete"
        logger.info(f"Crawling done for following URL: {url}")
    except Exception as e:
        logger.error(f"Error crawling {url}: {e}")
        task.status = "error"
        task.error_message = str(e)
    finally:
        task.save()
