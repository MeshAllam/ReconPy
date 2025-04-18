import concurrent.futures
import threading
from typing import List, Dict, Optional, Set
from pathlib import Path
from .dns_resolver import DNSResolver
from .word_generator import SubdomainWordGenerator
from .vulnerability_scanner import VulnerabilityScanner

class DomainEnumerator:
    def __init__(self, dns_servers: Optional[List[str]] = None,
                 recursive_depth: int = 3,
                 max_threads: int = 50,
                 wordlist_dir: str = "wordlists",
                 model_dir: str = "models"):
        self.dns_resolver = DNSResolver(dns_servers)
        self.recursive_depth = recursive_depth
        self.max_threads = max_threads
        self.word_generator = SubdomainWordGenerator(model_dir)
        self.checked_domains = set()
        self.lock = threading.Lock()

    def enumerate(self, domain: str) -> List[str]:
        self.checked_domains = set()
        found = set()

        if self._check_domain(domain):
            found.add(domain)

        found.update(self._recursive_enum(domain, current_depth=1))
        return sorted(found)

    def _recursive_enum(self, base_domain: str, current_depth: int) -> Set[str]:
        if current_depth > self.recursive_depth:
            return set()

        found = set()
        wordlist = self._get_wordlist_for_depth(base_domain, current_depth)

        new_subs = self.brute_force_with_custom_wordlist(base_domain, wordlist)
        found.update(new_subs)

        if new_subs and current_depth < self.recursive_depth:
            with self.lock:
                self.word_generator.train_model(list(new_subs))
                for sub in new_subs:
                    if sub not in self.checked_domains:
                        self.checked_domains.add(sub)
                        found.update(self._recursive_enum(sub, current_depth + 1))

        return found

    def brute_force_with_custom_wordlist(self, domain: str, wordlist: Set[str]) -> List[str]:
        found = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = {
                executor.submit(self._check_domain, f"{word}.{domain}"): word
                for word in wordlist
            }
            for future in concurrent.futures.as_completed(futures):
                word = futures[future]
                if future.result():
                    found_sub = f"{word}.{domain}"
                    found.append(found_sub)
        return found

    def _check_domain(self, domain: str) -> bool:
        return len(self.dns_resolver.resolve(domain)) > 0

    def _get_wordlist_for_depth(self, base_domain: str, depth: int) -> Set[str]:
        if depth == 1:
            return set(self._load_default_wordlist())
        parent_parts = base_domain.split('.')
        if len(parent_parts) <= 1:
            return set()
        similar_words = set()
        for part in parent_parts[:-1]:
            similar_words.update(self.word_generator.generate_similar_words(part))
        return similar_words

    def _load_default_wordlist(self) -> List[str]:
        default = ["www", "mail", "api", "dev", "admin", "test", "stage", "prod"]
        return default

    def check_takeovers(self, subdomains: List[str]) -> Dict[str, bool]:
        scanner = VulnerabilityScanner()
        results = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = {
                executor.submit(scanner.check_subdomain_takeover, sub): sub
                for sub in subdomains
            }
            for future in concurrent.futures.as_completed(futures):
                sub = futures[future]
                try:
                    results[sub] = future.result()
                except Exception as e:
                    results[sub] = False
        return results
