import requests
from bs4 import BeautifulSoup
import re
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import logging

logger = logging.getLogger(__name__)



def crawl_single_page(url):
    visited_links = set()

    try:

        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # 1. Page Title (H1)
        title = soup.find('h1').get_text() if soup.find('h1') else "No H1 found"
        logger.info(f"Crawling {title}:{url}")
        # 2. Page Summary (with Stemmer and Stop Words)
        # Extract the main content
        main_content = soup.find('div', {'id': 'mw-content-text'})

        # Remove unwanted elements
        for element in main_content(['table', 'sup']):
            element.decompose()

        # Get the full text
        full_text = main_content.get_text()

        parser = HtmlParser.from_string(full_text, url, Tokenizer("english"))
        stemmer = Stemmer("english")

        # Choose your summarizer:
        summarizer = LsaSummarizer(stemmer)
        summarizer.stop_words = get_stop_words("english")

        # Calculate target summary length (approx. 30%)
        target_length = int(len(full_text) * 0.3)

        # Determine sentence count for the target length
        sentence_count = 0
        current_length = 0
        for sentence in parser.document.sentences:
            current_length += len(sentence._text)
            sentence_count += 1
            if current_length >= target_length:
                break

        page_summary = ' '.join([str(sentence) for sentence in summarizer(parser.document, sentence_count)])

        # 3. Array of Links (with Regex and recursion prevention)
        link_pattern = re.compile(r'https?://[^\s]+\.[^\s]+')  # Regex for http/https links

        def extract_links(soup, base_url):
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.startswith('/'):
                    href = base_url + href
                if href not in visited_links and link_pattern.match(href):
                    visited_links.add(href)
                    yield href

        links = list(extract_links(soup, url))

        logger.info(f"Crawling {title} done...")

        return title, page_summary, links

    except Exception as error:
        logger.error(f"Crawling failed due to error: {error}")
        raise error



