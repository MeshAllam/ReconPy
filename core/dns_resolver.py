import dns.resolver
from typing import List, Optional
import socket

class DNSResolver:
    def __init__(self, nameservers: Optional[List[str]] = None):
        self.resolver = dns.resolver.Resolver()
        if nameservers:
            self.resolver.nameservers = nameservers
        self.resolver.timeout = 2
        self.resolver.lifetime = 2

    def resolve(self, domain: str, record_type: str = 'A') -> List[str]:
        try:
            answers = self.resolver.resolve(domain, record_type)
            return [str(r) for r in answers]
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
            return []
        except Exception as e:
            print(f"[!] DNS Error for {domain}: {e}")
            return []
