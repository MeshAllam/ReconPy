import requests
import concurrent.futures
from urllib.parse import urljoin
from pathlib import Path
from typing import List, Set, Dict
import re
import os
from tqdm import tqdm
import threading

class DirectoryBruteforcer:
    def __init__(self, wordlist_dir: str = "wordlists"):
        self.wordlist_dir = Path(wordlist_dir)
        self.wordlist_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'ReconPy'})
        self.lock = threading.Lock()

    def bruteforce(self, base_url: str, wordlist: List[str],
                  extensions: List[str] = None, threads: int = 20) -> Dict[str, int]:
        if not base_url.endswith('/'):
            base_url += '/'

        results = {}
        wordlist = self._expand_wordlist(wordlist, extensions or [''])

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = {
                executor.submit(self._check_path, base_url, path): path
                for path in wordlist
            }
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(wordlist)):
                path = futures[future]
                try:
                    status = future.result()
                    if status:
                        results[path] = status
                except Exception as e:
                    print(f"[!] Error checking {path}: {e}")

        if results:
            self._save_new_words(results.keys())
        return results

    def _check_path(self, base_url: str, path: str) -> int:
        url = urljoin(base_url, path)
        try:
            response = self.session.get(url, timeout=5)
            if response.status_code < 400:
                return response.status_code
        except requests.RequestException:
            pass
        return 0

    def _expand_wordlist(self, wordlist: List[str], extensions: List[str]) -> List[str]:
        expanded = []
        for word in wordlist:
            for ext in extensions:
                if ext:
                    expanded.append(f"{word}.{ext}")
                else:
                    expanded.append(word)
        return expanded

    def _save_new_words(self, paths: List[str]):
        new_words = set()
        for path in paths:
            parts = path.split('/')
            for part in parts:
                base = part.split('.')[0]
                if len(base) > 2:
                    new_words.add(base)

        if new_words:
            with self.lock:
                with open(self.wordlist_dir / "generated.txt", 'a') as f:
                    f.write('\n'.join(new_words) + '\n')
