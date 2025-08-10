import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import concurrent.futures
import time

def validate_url(url, config):
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return False, "Please enter a valid URL with http:// or https://"
    return True, "URL format is valid"

def extract_main_content(soup):
    main_selectors = [
        'main', 'article', '[role="main"]', 
        '.content', '.post-content', '.entry-content',
        '#content', '#main-content', '.main-content'
    ]
    
    for selector in main_selectors:
        main_content = soup.select_one(selector)
        if main_content:
            return main_content
    
    text_containers = soup.find_all(['div', 'section', 'article'])
    if text_containers:
        largest = max(text_containers, key=lambda x: len(x.get_text(strip=True)))
        if len(largest.get_text(strip=True)) > 200:
            return largest
    
    return soup.find('body') or soup

def fast_clean_text(element):
    for tag in element.find_all(['script', 'style', 'nav', 'header', 'footer', 'aside', 'form', 'button']):
        tag.decompose()
    
    text = element.get_text(separator=' ', strip=True)
    
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return ' '.join(lines)

def fetch_and_clean_content(url, config):
    start_time = time.time()
    
    try:
        headers = {
            "User-Agent": config["scraping"]["user_agent"],
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive"
        }
        
        timeout = min(config["scraping"]["timeout"], 10)
        
        response = requests.get(
            url, 
            headers=headers, 
            timeout=timeout,
            stream=True
        )
        response.raise_for_status()
        
        max_size = config["scraping"]["max_content_size"]
        content = response.content[:max_size]
        
        try:
            soup = BeautifulSoup(content, 'lxml')
        except:
            soup = BeautifulSoup(content, 'html.parser')
        
        main_content = extract_main_content(soup)
        text = fast_clean_text(main_content)
        
        max_chars = config["scraping"]["max_text_chars"]
        if len(text) > max_chars:
            text = text[:max_chars] + "..."
        
        if len(text.strip()) < 50:
            return None, "No readable content found on the page"
        
        processing_time = time.time() - start_time
        print(f"⚡ Scraped in {processing_time:.2f}s - {len(text)} chars")
        
        return text, None
        
    except requests.exceptions.Timeout:
        return None, "Page took too long to load"
    except requests.exceptions.RequestException as e:
        return None, f"Failed to fetch page: {str(e)}"
    except Exception as e:
        return None, f"Error processing page: {str(e)}"
