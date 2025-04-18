import requests
import json
from typing import List, Dict
from urllib.parse import urlparse, parse_qs
from tqdm import tqdm
import time

class WaybackScraper:
    def __init__(self, config: dict):
        self.api_url = "http://web.archive.org/cdx/search/cdx"
        self.timeout = config.get('timeout', 30)
        self.max_urls = config.get('max_urls', 10000)
        self.request_delay = config.get('request_delay', 1)

    def get_all_urls(self, domain: str) -> List[str]:
        params = {
            'url': domain,
            'output': 'json',
            'fl': 'original',
            'limit': self.max_urls
        }

        try:
            time.sleep(self.request_delay)
            response = requests.get(self.api_url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            return list(set(url[0] for url in data[1:] if url))  # Skip header row
        except Exception as e:
            print(f"[!] Wayback Machine error: {e}")
            return []

    def extract_parameters(self, urls: List[str]) -> Dict[str, List[str]]:
        params = {}
        for url in tqdm(urls, desc="Extracting parameters"):
            try:
                query = urlparse(url).query
                if query:
                    for param in parse_qs(query).keys():
                        params.setdefault(param, []).append(url)
            except:
                continue
        return params
