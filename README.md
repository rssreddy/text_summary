# Django Web Scraper and Summarizer

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://www.example.com) [![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

This Django project provides a powerful tool for scraping web pages, extracting their core content, and summarizing it using advanced natural language processing techniques. It offers both a single-page scraping interface and an asynchronous bulk crawling API.

## Features

- **Web Page Scraping:** Extract page titles (H1), summaries, and links from any valid URL.
- **Summarization:** Utilize the Latent Dirichlet Allocation (LDA) algorithm for intelligent content summarization, condensing articles while preserving key information.
- **Link Filtering:** Employ regular expressions to filter and validate links for increased security and accuracy.
- **Async Bulk Crawling:** Submit multiple URLs for background processing and receive results via a separate API endpoint.
- **Progress Tracking:** Monitor the status of bulk crawl tasks ("pending," "in progress," "completed") and retrieve results when finished.


## Installation

1.  **Clone the Repository:**

   `git clone https://github.com/rssreddy/text_summary.git`
  ` cd text_summary`

2. **Create a Virtual Environment:**

   ``python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate``
3. Install Dependencies:

    `pip install -r requirements.txt`

4. Setup Celery: (For background tasks)
   * Install and configure Celery and a message broker (e.g., RabbitMQ or Redis). See the Celery documentation for details.

5. Database Migrations:

    `python manage.py migrate`

6. Run the Development Server:
    `uvicorn text_summary.asgi:application`

